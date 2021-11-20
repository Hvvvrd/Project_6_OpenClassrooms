#!/usr/bin/python
#-*-coding: utf-8 -*

#########################################
########### Importation modules #########
#########################################

import sys, getopt
import fileinput
import os
from socket import *
import yaml
import os.path
import configparser

###################################################
###########Partie complétion des éléments #########
###################################################

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

###################################################
###########Partie configuration du DHCP	###########
###################################################

def dhcp_conf(server_name,subnet_mask,domain,option_dns,sous_res,interfaces):
	os.system("apt-get install isc-dhcp-server")

	fichier = open("/etc/dhcp/dhcpd.conf","w")
	fichier.write("##### Option générale par défaut #####\n")
	fichier.write("\n### RÉSEAU #####\n")
	fichier.write("\nserver-name \""+server_name+"\";") #nom du serveur dns
	fichier.write("\nauthoritative;")
	fichier.write("\noption subnet-mask "+subnet_mask+";")
	fichier.write("\noption domain-name \""+ domain +"\";")
	fichier.write("\noption domain-name-servers "+ option_dns +";")
	fichier.write("\nddns-update-style none;")
	fichier.write("\ndefault-lease-time 3600;")
	fichier.write("\nmax-lease-time 7200;")
	fichier.write("\nlog-facility local7;\n")
	fichier.write("\n##### RÉSEAUX #####\n")
	fichier.write("\n## Déclaration sous réseaux")

	interfaces= ''
	config = configparser.RawConfigParser() # On créé un nouvel objet "config"
	config.read('dhcp_reseau.ini')

	i=0
	for i in range(0,sous_res):

		reseau = str("reseau"+str(i))
		subnet = config.get(reseau,'subnet')
		netmask = config.get(reseau,'netmask')
		broadcast = config.get(reseau,'broadcast')
		ntp = config.get(reseau,'ntp')
		routers = config.get(reseau,'routers')
		pool = config.get(reseau,'pool')

		fichier.write("\nsubnet "+subnet+" netmask "+netmask+" {")
		fichier.write("\n  option domain-name \""+domain+"\";")
		fichier.write("\n  option broadcast-address "+broadcast+";")
		fichier.write("\n  option ntp-servers "+ntp+";")
		fichier.write("\n  option routers "+routers+";")
		fichier.write("\n  range "+pool+";")
		fichier.write("\n  ping-check = 1;")
		fichier.write("\n}\n")
	fichier.close()

	replaceAll("/etc/default/isc-dhcp-server","INTERFACESv4=\"\"","INTERFACESv4=\""+interfaces+"\"")
	os.system("service isc-dhcp-server restart")

###################################################
########### Partie configuration du DNS	###########
###################################################

def dns_conf(domain,ip):
	os.system("apt-get install bind9")
	os.system("cp /etc/bind/db.local /etc/bind/"+domain)
		
	a = open("/etc/bind/named.conf.local","w")
	a.write("\nzone \""+domain+"\" {\n")
	a.write("	type master;\n")
	a.write("	file \"/etc/bind/"+domain+"\";\n")
	a.write("	allow-query { any; };\n")
	a.write("};")
	a.close()

	replaceAll("/etc/bind/"+domain,"localhost. root.localhost.","ns.site."+domain+". root."+domain+".")
	replaceAll("/etc/bind/"+domain,"localhost.","ns")
	replaceAll("/etc/bind/"+domain,"127.0.0.1",ip)
	replaceAll("/etc/bind/"+domain,"@	IN	AAAA	::1","ns	IN	A	"+ip)	
	f=open("/etc/bind/"+domain,"a")
	f.write("www	IN	A	"+ip)
	f.write("\nmailx	IN	A	"+ip)
	f.write("\n@	IN MX 100 mailx."+domain+".")
	f.close()
	os.system("service bind9 restart")

###################################
###########	main	###########
###################################

def main(argv):

   domain = ''
   ip = ''
   server_name = ''
   subnet_mask = ''
   option_dns = ''
   sous_res = ''
   interfaces = ''

   try:
      opts, args = getopt.getopt(argv,"hid:a:n:m:o:r:f:",["domain=","addr=","name=","mask=","optdns=","reseau=","interfaces="])
   except getopt.GetoptError:
      print ('dhcp_dns.py -i pour le mode interactif ou dhcp_dns.py -d <domain> -a <addr ip> -n <server name> -m <subnet mask> -o <option dns> -r <nb sous res> --interfaces="interface1 interface2 or_more"')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('dhcp_dns.py -i mode interactif ou dhcp_dns.py -d <domain> -a <addr ip> -n <server name> -m <subnet mask> -o <option dns> -r <nb sous res> --interfaces="interface1 interface2 or_more"')
         sys.exit()
      elif opt in ("-d", "--domain"):
         domain = arg
      elif opt in ("-a", "--addr"):
         ip = arg
      elif opt in ("-n", "--name"):
         server_name = arg
      elif opt in ("-m", "--mask"):
         subnet_mask = arg
      elif opt in ("-o", "--optdns"):
         option_dns = arg
      elif opt in ("-r", "--reseau"):
         sous_res = int(arg)
      elif opt in ("-f", "--interfaces"):
         interfaces = arg
      elif opt in ("-i", "--i"):
         domain = input("Entrez le nom de domaine : ")
         ip = input("Entrez l'ip du serveur dns : ")
         server_name = input("Entrez le nom du serveur DHCP : ") 
         subnet_mask = input("Entrez le masque : ")
         option_dns = input("Entrez les options dns : ")
         sous_res=int(input("Entrez le nombre de sous réseaux : "))
         interfaces=input("Entrez les interfaces d'écoute : ")
   dns_conf(domain,ip)
   dhcp_conf(server_name,subnet_mask,domain,option_dns,sous_res,interfaces)


if __name__ == "__main__":
   main(sys.argv[1:])
