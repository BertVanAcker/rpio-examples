from ship_maneuvering_model import ShipModel
import HydroPara_PI3_alternative1 as HydroPara_PI3
from aux_fuctions import *
import os


def main():
    model = ShipModel()

    verification_data = "Manuevering_Data_K_SIM\\No_Wind"
    dir_list = [os.path.join(verification_data, file) for file in os.listdir(verification_data)]

    # Testing model
    for file in dir_list:
        print(file)

        data = load_data(file, model.U0)
        data = data.shift(-30)

        # Make the trajectory prediction based on the initial conditions, rudder angle, wind direction and speed collected from the simulator
        eta, nu = model.predict(HydroPara_PI3, data['Surge Speed'][0], data['Sway Speed'][0], data['Yaw Rate'][0],
                                data['Heading'][0], data['x'][0], data['y'][0], data['Rudder Angle'],
                                data['Wind Direction'], data['Wind Speed'])

        make_plots(data, eta, nu)

if __name__ == "__main__":
    main()
