# Automation of Cisco Nexus 9000

## NETCONF
Preapre Cisco Nexus to be managed via NETCONF

### Enable NETCONF functionality
Configure:
```
c-1-s1(config)# feature netconf
```

Validate:
```
c-1-s1# show feature | grep netconf
netconf                1          enabled 
```

## GNMI
Preapre Cisco Nexus to be managed via GNMI

### Enable Bash
Configure:
```
c-1-s1(config)# feature bash-shell 
```

Validate:
```
```

### Create self-signed certificate
Enter the bash (from privileged mode)
```
c-1-s1# run bash sudo su
bash-4.3# 
```

Create certificate
```
bash-4.3# cd /bootflash
bash-4.3# openssl req -x509 -newkey rsa:2048 -keyout grpc_test.key -out grpc_test.pem -days 365 -nodes -subj '/CN=c-1-s1.lab.karneliuk.com'
bash-4.3# openssl pkcs12 -export -out grpc_test.pfx -inkey grpc_test.key -in grpc_test.pem -certfile grpc_test.pem -password pass:Pygnmi123!
bash-4.3# exit
```

### Import created self-signed cert
Configure:
```
c-1-s1(config)# crypto ca trustpoint grpc-test-ca
c-1-s1(config)# crypto ca import grpc-test-ca pkcs12 bootflash:///grpc_test.pfx Pygnmi123!
```

Validate:
```
c-1-s1# show crypto ca trustpoints
trustpoint: grpc-test-ca; key-pair: grpc-test-ca
revokation methods:  crl


c-1-s1# show crypto key mypubkey rsa 
key label: grpc-test-ca
key size: 2048
exportable: yes
key-pair already generated


c-1-s1# show crypto ca certificates grpc-test-ca
Trustpoint: grpc-test-ca
certificate:
subject= /CN=c-1-s1.lab.karneliuk.com
issuer= /CN=c-1-s1.lab.karneliuk.com
serial=F8319CA4D31F73FD
notBefore=Jul 24 14:34:40 2022 GMT
notAfter=Jul 24 14:34:40 2023 GMT
SHA1 Fingerprint=D7:D5:C8:2B:58:C4:9A:62:79:04:3F:09:05:A8:F4:A0:FB:8B:58:05
purposes: sslserver sslclient 

CA certificate 0:
subject= /CN=c-1-s1.lab.karneliuk.com
issuer= /CN=c-1-s1.lab.karneliuk.com
serial=F8319CA4D31F73FD
notBefore=Jul 24 14:34:40 2022 GMT
notAfter=Jul 24 14:34:40 2023 GMT
SHA1 Fingerprint=D7:D5:C8:2B:58:C4:9A:62:79:04:3F:09:05:A8:F4:A0:FB:8B:58:05
purposes: sslserver sslclient 

```

### Enable GRPC functionality
Configure:
```
c-1-s1(config)# feature grpc
```

Validate:
```
c-1-s1# show feature | grep 'grpc'
grpc                   1          enabled 
```

### Configure GRPC server
Configure:
```
c-1-s1(config)# grpc certificate grpc-test-ca
```

Validate:
```
c-1-s1# show grpc gnmi service statistics 

=============
gRPC Endpoint
=============

Vrf            : management
Server address : [::]:50051

Cert notBefore : Jul 24 14:34:40 2022 GMT
Cert notAfter  : Jul 24 14:34:40 2023 GMT

Max concurrent calls            :  8
Listen calls                    :  1
Active calls                    :  0

Number of created calls         :  1
Number of bad calls             :  0

Subscription stream/once/poll   :  0/0/0

Max gNMI::Get concurrent        :  5
Max grpc message size           :  8388608
gNMI Synchronous calls          :  0
gNMI Synchronous errors         :  0
gNMI Adapter errors             :  0
gNMI Dtx errors                 :  0
```