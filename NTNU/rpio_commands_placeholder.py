from rpio.transformations.transformations import swc2code_py,message2code_py
from rpio.parsers.parsers import AADL_parser

#-------------------------------------------------------------------------------------------------------
# !! THESE COMMANDS NORMALLY ARE CALLED FROM THE RPIO CLI, FOR TESTING PURPOSE, A PYTHON FILE IS USED !!
#-------------------------------------------------------------------------------------------------------

# 1. GENERATE AADL FROM ROBOARCH (NOT IMPLEMENTED YET)

# 2. GENERATE AADL INTERMEDIATE LANGUAGE FROM AADL
parser = AADL_parser(logicalArchitecture='Design/logicalArchitecture.aadl',physicalArchitecture='Design/physicalArchitecture',messages='Design/messages.aadl')
design = parser.aadl2aadlIl()
design.object2json(fileName='Design/system.json')

# 2. LOAD THE AADL INTERMEDUATE LANGUAGE (MOCKUP)
# design = HelloWorld()

# 3. GENERATE CUSTOM MESSAGES FROM AADL INTERMEDIATE LANGUAGE
try:
    message2code_py(system=design, path="Realization/ManagingSystem/Messages")
    message2code_py(system=design, path="Realization/ManagedSystem/Messages")
except:
    print("Failed to generate the messages")

# 4. GENERATE SWC CODE FROM AADL INTERMEDIATE LANGUAGE
try:
    swc2code_py(system=design,path="Realization/ManagingSystem/Nodes")
except:
    print("Failed to generate the software components")
