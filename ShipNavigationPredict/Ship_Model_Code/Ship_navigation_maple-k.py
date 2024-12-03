from rpio.clientLibraries.rpclpy.node import Node
import time
#analysis
import ship_maneuvering_model
import HydroPara_PI3_alternative1 as HydroPara_PI3
import numpy as np

#plan

import random

#execute 
import json

class Monitor(Node):

    def __init__(self, config='config.yaml',verbose=True):
        super().__init__(config=config,verbose=verbose)

        self._name = "Monitor"
        self.logger.info("Monitor instantiated")

        #<!-- cc_init START--!>
        # user includes here
        #<!-- cc_init END--!>
            # -----------------------------AUTO-GEN SKELETON FOR monitor_data-----------------------------
    def monitor_ship(self,msg):
        # _LaserScan = LaserScan()

        #<!-- cc_code_monitor_data START--!>

        # user code here for monitor_data

        # _LaserScan._ranges= "SET VALUE"    # datatype: Array
        # _LaserScan._angle_increment= "SET VALUE"    # datatype: Float_64

        #<!-- cc_code_monitor_data END--!>

        # _success = self.knowledge.write(cls=_LaserScan)
        self.knowledge.write("ship_status",msg)
        self.publish_event(event_key='/new_data')    # LINK <outport> new_data

    def monitor_weather(self,msg):
        # _LaserScan = LaserScan()

        #<!-- cc_code_monitor_data START--!>

        # user code here for monitor_data

        # _LaserScan._ranges= "SET VALUE"    # datatype: Array
        # _LaserScan._angle_increment= "SET VALUE"    # datatype: Float_64

        #<!-- cc_code_monitor_data END--!>

        # _success = self.knowledge.write(cls=_LaserScan)
        self.knowledge.write("weather_condition",msg)
        # self.publish_event(event_key='/new_data')    # LINK <outport> new_data

    def register_callbacks(self):
        self.register_event_callback(event_key='/ship_status', callback=self.monitor_ship)     # LINK <eventTrigger> Scan
        self.register_event_callback(event_key='/weather_condition', callback=self.monitor_weather)

def compare_trajectories(x, y, predicted_x, predicted_y):
    """
    Compare two trajectories given by x, y and predicted_x, predicted_y arrays,
    normalize the trajectories, and return a similarity score.

    Parameters:
        x: list or array of floats - Actual x coordinates
        y: list or array of floats - Actual y coordinates
        predicted_x: list or array of floats - Predicted x coordinates
        predicted_y: list or array of floats - Predicted y coordinates

    Returns:
        similarity_score: float - A score representing similarity (higher is better)
    """
    # Ensure all input arrays have the same length
    if len(x) != len(y) or len(y) != len(predicted_x) or len(predicted_x) != len(predicted_y):
        raise ValueError("All input arrays must have the same length")

    # Convert inputs to numpy arrays
    x = np.array(x)
    y = np.array(y)
    predicted_x = np.array(predicted_x)
    predicted_y = np.array(predicted_y)

    # Normalize the trajectories to fit in a unit square (0 to 1 range)
    def normalize(arr1, arr2):
        min_val = min(arr1.min(), arr2.min())  # Find the minimum value across both arrays
        max_val = max(arr1.max(), arr2.max())  # Find the maximum value across both arrays
        range_val = max_val - min_val         # Calculate the range
        if range_val == 0:                    # Handle edge case where all values are the same
            return arr1, arr2
        return (arr1 - min_val) / range_val, (arr2 - min_val) / range_val

    # Normalize x and predicted_x
    x, predicted_x = normalize(x, predicted_x)

    # Normalize y and predicted_y
    y, predicted_y = normalize(y, predicted_y)

    # Combine x and y into coordinate pairs
    actual = np.array(list(zip(x, y)))
    predicted = np.array(list(zip(predicted_x, predicted_y)))

    # Calculate Euclidean distances between corresponding points
    distances = np.linalg.norm(actual - predicted, axis=1)

    # Compute the similarity score (1 / (1 + average distance))
    average_distance = np.mean(distances)
    similarity_score = 1 / (1 + average_distance)  # Higher score means more similar

    return similarity_score

class Analysis(Node):

    def __init__(self, config='config.yaml',verbose=True):
        super().__init__(config=config,verbose=verbose)

        self._name = "Analysis"
        self.logger.info("Analysis instantiated")

        #<!-- cc_init START--!>
        self.anomaly = False
        self.ship_model = None
        

        # def scans():
        #     while True:
        #         for scan in self._scans:
        #             yield scan

        #         self._scans = []

        # def raw_lidar_masks():
        #     for scan in scans():
        #         yield lidar_mask_from_scan(scan)

        # self._sliding_prob_lidar_masks = sliding_prob_lidar_mask(
        #     raw_lidar_masks(),
        #     window_size=SLIDING_WINDOW_SIZE,
        # )
        #<!-- cc_init END--!>

    # -----------------------------AUTO-GEN SKELETON FOR analyse_scan_data-----------------------------
    def analyse_prediction_trajectory(self,msg):
        ship_status = self.knowledge.read("ship_status",queueSize=1)
        weather_condition = self.knowledge.read("weather_condition")
        


        #<!-- cc_code_analyse_scan_data START--!>

        # self.logger.info(f"REtrieved laser_scan: {self.lidar_data}")
        self.ship_model = getattr(ship_maneuvering_model,ship_status["ship_prediction_model"])()
        eta, nu =self.ship_model.predict(HydroPara_PI3,
            ship_status['Surge Speed'],
            ship_status['Sway Speed'],
            ship_status['Yaw Rate'],
            ship_status['Heading'],
            ship_status['x'][0],
            ship_status['y'][0],
            weather_condition['Rudder Angle'],
            weather_condition['Wind Direction'],
            weather_condition['Wind Speed'])
        window_size = 300 # 60 sample equals to 1 minute       
        score = compare_trajectories(ship_status['x'][0 : window_size],ship_status['y'][0 : window_size],eta[0 : window_size, 0], eta[0 : window_size, 1]  ) 
        # Set the monitor status to mark an anomaly if the there is any

        # # occlusion outside of the ignored region
        anomaly_status_old = self.anomaly
        if score: 
            if score > 0.97 : 
                self.anomaly = False
                self.logger.info(f" Anomaly: {self.anomaly}, similarity score is:{score}")
            else: 
                self.anomaly = True
                self.logger.info(f" Anomaly: {self.anomaly}, similarity score is:{score}")
            if anomaly_status_old != self.anomaly:
                if (self.anomaly == True):
                    self.publish_event(event_key='/anomaly')

        #<!-- cc_code_analyse_scan_data END--!>

        # self.publish_event(event_key='anomaly')    # LINK <outport> anomaly

    def register_callbacks(self):
        self.register_event_callback(event_key='/new_data', callback=self.analyse_prediction_trajectory)     # LINK <eventTrigger> new_data


class Plan(Node):

    def __init__(self, config='config.yaml',verbose=True):
        super().__init__(config=config,verbose=verbose)

        self._name = "Plan"
        self.logger.info("Plan instantiated")
        



    def planner(self,msg):

        ship_status = self.knowledge.read("ship_status",queueSize=1)
        
        # List of available models
        available_models = ["ShipModel_M1", "ShipModel_M2", "ShipModel_M7", "ShipModel_M12", "ShipModel_MS"]

        filtered_models = [s for s in available_models if s != ship_status['ship_prediction_model']]

        new_model = random.choice(filtered_models)
        self.knowledge.write("new_model", new_model)

        self.publish_event("/new_plan")
        

    def register_callbacks(self):
        self.register_event_callback(event_key='/anomaly', callback=self.planner)     # LINK <eventTrigger> anomaly

class Legitimate(Node):

    def __init__(self, config='config.yaml',verbose=True):
        super().__init__(config=config,verbose=verbose)

        self._name = "Legitimate"
        self.logger.info("Legitimate instantiated")

        #<!-- cc_init START--!>
        # user includes here
        #<!-- cc_init END--!>



class Execute(Node):

    def __init__(self, config='config.yaml',verbose=True):
        super().__init__(config=config,verbose=verbose)

        self._name = "Execute"
        self.logger.info("Execute instantiated")

        #<!-- cc_init START--!>
        # user includes here
        #<!-- cc_init END--!>

    # -----------------------------AUTO-GEN SKELETON FOR executer-----------------------------
    def executer(self,msg):

        # _Direction = Direction()

        #<!-- cc_code_executer START--!>

        # user code here for executer
        self.register_callbacks

        #<!-- cc_code_executer END--!>
        model = self.knowledge.read('new_model')
        self.publish_event(event_key='/new_model',message=model)    # LINK <outport> spin_config

    def register_callbacks(self):
        self.register_event_callback(event_key='/new_plan', callback=self.executer)        # LINK <inport> new_plan
        # self.register_event_callback(event_key='isLegit', callback=self.executer)        # LINK <inport> isLegit

def main(args=None):

    node = Legitimate(config='config.yaml')
    node.start()

def main(args=None):
    monitor_node = Monitor(config='config_m.yaml')
    monitor_node.register_callbacks()
    monitor_node.start()

    analysis_node = Analysis(config='config_a.yaml')
    analysis_node.register_callbacks()
    analysis_node.start()

    plan_node = Plan(config='config_p.yaml')
    plan_node.register_callbacks()
    plan_node.start()

    
    # legitimate_node = Legitimate(config='config_l.yaml')
    # legitimate_node.start()

    execute_node = Execute(config='config_e.yaml')
    execute_node.register_callbacks()
    execute_node.start()


if __name__ == '__main__':
    main()
    try:
       while True:
           time.sleep(1)
    except:
       exit()