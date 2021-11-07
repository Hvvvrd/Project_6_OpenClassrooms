# Project_6_OpenClassrooms
Projet 6 "Participation à la vie de la communauté Open Source" du parcours Administrateur Infrastructure &amp; Cloud d'OpenClassrooms

##Présentation
L'objectif de ce projet est de proposer un script qui permet d'automatiser la configuration DHCP et DNS d'un serveur sous Linux Ubuntu rapidement.

Ce script propose deux modes de lancement :
- mode interactif : sudo dhcp_dns.py -i 
- mode argument : sudo dhcp_dns.py -d <domain> -a <addr ip> -n <server name> -m <subnet mask> -o <option dns> -r <nombre de sous-réseaux> --interfaces=<"interface1 interface2 ..."> 

La différence entre les deux modes étant que le mode argument la valeur des variables est mentionné directement dans les arguments tandis que, le mode interactif proposera de saisir les valeurs dans le terminal, au fur et à mesure, de la configuration du script, en réponse à une interaction avec l'utilisateur, sous-forme de questions. Pour cela, il suffira de saisir dans le terminal la valeur souhaitée et de faire « entrer ».

Les paramètres que nous retrouvons pour notre script script_config_dhcp_dns.py sont :
```
-h : aide 
-i : lancer le mode interactif
-d : rentrer votre nom de domaine dns (ex : mon-entreprise.fr)
-a : rentrer votre adresse IP (ex : 10.0.1.2)
-n : rentrer votre nom de serveur dhcp (ex : ubuntu.lan)
-m : rentrer votre masque pour le serveur (ex : 255.255.255.0)
-o : rentrer les options dns (ex : 8.8.8.8, 1.1.1.1)
-r : rentrer le nombre de sous réseau que vous avez configuré dans le fichier res.ini
--interfaces : rentrer vos interfaces d'écoute du serveur dhcp (ex : "enp0s3 enp0s8")
```
Notre script script_config_dhcp_dns.py est accompagné d'un second fichier : res.ini. Ce second fichier doit se trouver impérativement dans le même répertoire que dhcp_dns .py. Dedans, il sera déclarer nos sous-réseaux de la façons suivante, en prenant exemple ici pour 2 sous-réseaux :
```
[reseau0]
subnet: 10.0.0.0
netmask: 255.255.255.0
broadcast: 10.0.0.255
ntp: 10.0.0.1
routers: 10.0.0.1
pool: 10.0.0.2 10.0.0.254

[reseau1]
subnet: 10.0.0.0
netmask: 255.255.255.0
broadcast: 10.0.0.255
ntp: 10.0.0.1
routers: 10.0.0.1
pool: 10.0.0.2 10.0.0.254
```
A noter, si nous prenons notre exemple pour 2 sous-réseaux, que lors de l'exécution du mode argument de notre script, l'argument -r <nombre de sous-réseaux> sera donc -r 2.
  
##Fonctionnement 
