
import sys
import os
import os.path
import shutil
import math

print "\nPython utility for generating ChannelML based synapse for given name, conductance etc. "

origCmd = ""
for arg in sys.argv: origCmd = origCmd+" "+arg

if len(sys.argv) is not 5:
    print "Usage:\n   python   genSyn.py   Syn_AMPA_TCR_nRT   tau_in_ms   scaling_in_nS   rev_pot_in_mV  \n"
    exit()

name = sys.argv[1]
tau = float(sys.argv[2])
scaling = float(sys.argv[3])
rev_pot = float(sys.argv[4])

chemical_syn_attrs = "max_conductance=\"MAX_COND\" rise_time=\"TAU_RISE\" decay_time=\"TAU_DECAY\" reversal_potential=\"REV_POT\""
electrical_syn_attrs = "conductance=\"GAP_COND\""
block_info = ""

max_cond = -1
cond = -1
tau_rise = -1
tau_decay = -1

if "AMPA" in name:
    max_cond = 1e-6 * scaling * tau / math.e
    tau_rise = tau
    tau_decay = tau
    cml_syn_element="doub_exp_syn"
    cml_syn_attrs = chemical_syn_attrs

elif "NMDA" in name :
    max_cond = 1e-6 * scaling
    tau_rise = 1
    tau_decay = tau
    cml_syn_element="blocking_syn"
    cml_syn_attrs = chemical_syn_attrs
    block_info = "            <block species=\"mg\" conc=\"1.5e-6\" eta=\"0.280112e6\" gamma=\"0.062\"/>  <!-- Taken from eqn (5) Jahr & Stevens 1990 -->\n\n"

elif "GABAA" in name:
    max_cond = 1e-6 * scaling
    tau_rise = 0
    tau_decay = tau
    cml_syn_element="doub_exp_syn"
    cml_syn_attrs = chemical_syn_attrs

elif "Elect" in name:
    cond = 1e-6 * scaling
    cml_syn_element="electrical_syn"
    cml_syn_attrs = electrical_syn_attrs




print "Creating a synapse mechanism: %s with time course val: %f ms, and syn scaling %f nS" % (name, tau, scaling)


desc = "Synapse with syn scaling constant c = %g nS (translating to max cond of %g mS), time course: %g ms and reversal potential: %g mV." % (scaling, max_cond, tau, rev_pot)
if "Elect" in name:
    desc = "Electrical synapse with scaling constant c = %g nS (translating to conductance of %g mS)." % (scaling, cond)
    
desc = desc + "\n        Automatically generated by command: %s " % (origCmd)

print desc

cellMechsDir = "../../cellMechanisms/"
cellMechDir = cellMechsDir+name

if os.path.exists(cellMechDir):

    if os.path.exists("overwrite"):
            shutil.rmtree(cellMechDir)
    else:
        ans = raw_input("Directory %s exists! Overwrite (y/all/n)?"% cellMechDir)
        if ans is "y":
            shutil.rmtree(cellMechDir)
        elif "all" in ans:
            shutil.rmtree(cellMechDir)
            print "Overwriting files always..."
            ov = open("overwrite",'w')
            ov.write("all")
            ov.close()
        else:
            print "Closing and not overwriting files..."
            exit()

os.makedirs(cellMechDir)


cmlSynXmlFilename = "ChannelMLSyn.xml"
propsFilename = "properties.xml"
neuronFilename= "ChannelML_v1.8.1_NEURONmod.xsl"
genesisFilename= "ChannelML_v1.8.1_GENESIStab.xsl"
xslLocation = "../../../../templates/xmlTemplates/Schemata/v1.8.1/Level2/"

if not os.path.exists(xslLocation):
    xslLocation = os.getenv("HOME")+"/neuroConstruct/templates/xmlTemplates/Schemata/v1.8.1/Level2/"

props = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"+ \
"<!DOCTYPE properties SYSTEM \"http://java.sun.com/dtd/properties.dtd\">"+\
"<properties>\n"+\
"<entry key=\"Description\">DESC</entry>\n"+\
"<entry key=\"NEURON mapping\">"+neuronFilename+"</entry>\n"+\
"<entry key=\"GENESIS mapping\">"+genesisFilename+"</entry>\n"+\
"<entry key=\"Implementation method\">ChannelML based Cell Mechanism</entry>\n"+\
"<entry key=\"NEURON file requires compilation\">true</entry>\n"+\
"<entry key=\"Mechanism Type\">Synaptic mechanism</entry>\n"+\
"<entry key=\"ChannelML file\">"+cmlSynXmlFilename+"</entry>\n"+\
"<entry key=\"GENESIS file requires compilation\">true</entry>\n"+\
"<entry key=\"Mechanism Name\">NAME</entry>\n"+\
"<entry key=\"Mechanism Model\">ChannelML based process</entry>\n"+\
"</properties>"

cml="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"+ \
"<channelml xmlns=\"http://morphml.org/channelml/schema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:meta=\"http://morphml.org/metadata/schema\" "+\
"xsi:schemaLocation=\"http://morphml.org/channelml/schema  http://www.neuroml.org/NeuroMLValidator/NeuroMLFiles/Schemata/v1.8.1/Level2/ChannelML_v1.8.1.xsd\" units=\"Physiological Units\">"+\
"\n\n"+ \
"    <meta:notes>ChannelML file describing a single synaptic mechanism</meta:notes>\n"+ \
"\n"+ \
"    <synapse_type name=\"NAME\">\n"+ \
"\n"+ \
"        <status value=\"stable\"><meta:contributor><meta:name>Padraig Gleeson</meta:name></meta:contributor></status>\n"+ \
"\n"+ \
"        <meta:notes>NOTES</meta:notes>\n"+ \
"\n"+ \
"        <"+cml_syn_element+" "+cml_syn_attrs+">\n"+ \
"\n"+ \
block_info+\
"        </"+cml_syn_element+">\n"+ \
"\n"+ \
"    </synapse_type>\n"+ \
"\n"+ \
"</channelml>\n"



props = props.replace("NAME", name)
props = props.replace("DESC", desc)

propsFile = open(cellMechDir+"/"+propsFilename, mode='w')
propsFile.write(props)
propsFile.close()

cml = cml.replace("NAME", name)
cml = cml.replace("NOTES", desc)
cml = cml.replace("MAX_COND", str(max_cond))
cml = cml.replace("GAP_COND", str(cond))
cml = cml.replace("TAU_RISE", str(tau_rise))
cml = cml.replace("TAU_DECAY", str(tau_decay))
cml = cml.replace("REV_POT", str(rev_pot))


cmlFile = open(cellMechDir+"/"+cmlSynXmlFilename, mode='w')
cmlFile.write(cml)
cmlFile.close()

neuronFile = os.path.abspath(xslLocation+neuronFilename)
print "Copying %s to directory %s " % (neuronFile, cellMechDir)
shutil.copy(neuronFile, cellMechDir)

genesisFile = os.path.abspath(xslLocation+genesisFilename)
print "Copying %s to directory %s " % (genesisFile, cellMechDir)
shutil.copy(genesisFile, cellMechDir)



print "Done!\n"

