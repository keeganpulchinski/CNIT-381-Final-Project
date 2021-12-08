import netmiko
from ncclient import manager 
import xml.dom.minidom
 
m = manager.connect(
         host="192.168.56.101",     
         port=830,     
         username="cisco",     
         password="cisco",     
         hostkey_verify=False 
    ) 

''' 
print("#Supported Capabilities (YANG models):") 
for capability in m.server_capabilities: 
    print(capability) 
'''

netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>R1</hostname>
  </native>
</config>
"""

netconf_filter = """ 
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface>
    <name>Loopback0</name>
  </interface>
</interfaces>                
""" 

netconf_filter2 = """
 <rpc message-id="101"
          xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <get>
         <filter type="subtree">
             <interfacesxmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
               <interface>
                 <Name>Loopback0</Name>
               </interface>
             </interfaces>
         </filter>
       </get>
     </rpc>
""" 

netconf_newloop = """ 
<config> 
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"> 
  <interface> 
   <Loopback> 
    <name>0</name> 
    <description>My Second NETCONF loopback</description> 
    <ip> 
     <address> 
      <primary> 
       <address>100.10.10.2</address> 
       <mask>255.255.253.0</mask> 
      </primary> 
     </address> 
    </ip> 
   </Loopback> 
  </interface> 
 </native> 
</config> 
""" 
net_user = """
<username xmlns="urn:opendaylight:netconf-node-topology">admin</username>
  <password xmlns="urn:opendaylight:netconf-node-topology">admin</password>
"""


netconf_reply = m.get_config(source="running") 
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
netconf_reply = m.get_config(source="running", filter=('subtree',netconf_filter2)) 
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
netconf_reply = m.edit_config(target="running", config=netconf_hostname) 
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
netconf_reply = m.edit_config(target="running", config=netconf_newloop)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
netconf_reply = m.edit_config(target="running", config=netconf_newloop) 
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()) 



