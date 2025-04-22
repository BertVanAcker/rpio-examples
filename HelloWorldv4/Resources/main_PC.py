from HelloWorldv4.Realization.ManagingSystem.Nodes.Monitor.Monitor import Monitor
from HelloWorldv4.Realization.ManagingSystem.Nodes.Analysis.Analysis import Analysis
from HelloWorldv4.Realization.ManagingSystem.Nodes.Plan.Plan import Plan
from HelloWorldv4.Realization.ManagingSystem.Nodes.Legitimate.Legitimate import Legitimate
from HelloWorldv4.Realization.ManagingSystem.Nodes.Execute.Execute import Execute
from HelloWorldv4.Realization.ManagingSystem.Nodes.Trustworthiness.Trustworthiness import Trustworthiness
import time

_Monitor = Monitor("../Realization/ManagingSystem/Nodes/Monitor/config.yaml")
_Analysis = Analysis("../Realization/ManagingSystem/Nodes/Analysis/config.yaml")
_Plan = Plan("../Realization/ManagingSystem/Nodes/Plan/config.yaml")
_Legitimate = Legitimate("../Realization/ManagingSystem/Nodes/Legitimate/config.yaml")
_Execute = Execute("../Realization/ManagingSystem/Nodes/Execute/config.yaml")
_Trustworthiness = Trustworthiness("../Realization/ManagingSystem/Nodes/Trustworthiness/config.yaml")

_Monitor.register_callbacks()
_Analysis.register_callbacks()
_Plan.register_callbacks()
_Legitimate.register_callbacks()
_Execute.register_callbacks()
_Trustworthiness.register_callbacks()

_Monitor.start()
_Analysis.start()
_Plan.start()
_Legitimate.start()
_Execute.start()
_Trustworthiness.start()

try:
    print("Script is running. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)  # Sleep to avoid busy-waiting
except KeyboardInterrupt:
    _Monitor.shutdown()
    _Analysis.shutdown()
    _Plan.shutdown()
    _Legitimate.shutdown()
    _Execute.shutdown()
    _Trustworthiness.shutdown()
    print("\nKeyboard interruption detected. Exiting...")