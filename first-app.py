import streamlit as st

def valid_ip_address(ip):
    ip_octets = ip.split('.')
    result = all(int(num) > 0 and int(num)<255 for num in ip_octets)
    return result
    


def binary_to_ip(ip_binary):
    ip_binary_octets = [str(int(ip_binary[8*i:8*i+8],2)) for i in range(4)]
    ip_doted_decimal = '.'.join(ip_binary_octets)
    return(ip_doted_decimal)

def calculate_subnet_details(ipaddress,mask):
    subnet_mask_binary = '1' * mask + '0' * (32 - mask)
    first_usable_host_ip_portion = '0' * (32 - mask-1) + '1'
    last_usable_host_ip_portion = '1' * (32 - mask-1) + '0'
    subnet_broadcast = '1' * (32 - mask)
    
    subnet_mask_doted_decimal = binary_to_ip(subnet_mask_binary)
    
    ip_octets = ipaddress.split('.')
    subnet_octets = subnet_mask_doted_decimal.split('.')
    
    netword_id = [int(ip_octets[i]) & int(subnet_octets[i]) for i in range(4)]
    network_id_doted_decimal = '.'.join(str(i) for i in netword_id)
    network_id_binary = [format(i,'08b') for i in netword_id]
    network_portion = ''.join(str(i) for i in network_id_binary)[:mask]
    first_usable_ip = binary_to_ip(network_portion+first_usable_host_ip_portion)
    last_usable_ip = binary_to_ip(network_portion+last_usable_host_ip_portion)
    subnet_broadcast_ip = binary_to_ip(network_portion+subnet_broadcast)
    subnet_details = []
    subnet_details.append(network_id_doted_decimal)
    subnet_details.append(first_usable_ip)
    subnet_details.append(last_usable_ip)
    subnet_details.append(subnet_broadcast_ip)
    subnet_details.append(subnet_mask_doted_decimal)
    return(subnet_details)


st.header('IPv4 Subnet Calculator')

ipAddress = st.text_input('Enter a Valid IP Address')
mask = st.slider('Select Subnet mask',min_value=8, max_value=30)
genNetwork = st.button('Get Details')
if(genNetwork):
    if ipAddress == "":
        st.warning("Please enter IP Address.")
    else:
        ip_address_validity = valid_ip_address(ipAddress)
        if ip_address_validity:
            network_details = calculate_subnet_details(ipAddress,mask)
            st.success(f'''
                        Network Address : {network_details[0]}  
                        Usable IP Range : {network_details[1]} - {network_details[2]}  
                        Broadcast IP : {network_details[3]}  
                        Subnet Mask : {network_details[-1]}
                        ''')

            
        else:
            st.error('Enter a Valid IP Address.')

