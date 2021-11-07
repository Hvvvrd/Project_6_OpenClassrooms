# Project_6_OpenClassrooms
Projet 6 "Participation à la vie de la communauté Open Source" du parcours Administrateur Infrastructure &amp; Cloud d'OpenClassrooms
par Vivien HAVARD

Nous portons à l'intention du lecteur la mise à disposition d'une documentation technique rentrant dans les détails sur le projet, les choix et la rédaction de notre script consultable dans notre répertoire GitHub : Documentation_technique.pdf

## Présentation du fonctionnement de notre script
L'objectif de ce projet est de proposer un script qui permet d'automatiser la configuration DHCP et DNS d'un serveur sous Linux Ubuntu rapidement.

Ce script propose deux modes de lancement :
```
- mode interactif : sudo script_config_dhcp_dns.py -i 
- mode argument : sudo script_config_dhcp_dns.py -d <domain> -a <addr ip> -n <server name> -m <subnet mask> -o <option dns> -r <nombre de sous-réseaux> --interfaces=<"interface1 interface2 ..."> 
```
La différence entre les deux modes étant que le mode argument la valeur des variables est mentionné directement dans les arguments tandis que, le mode interactif proposera de saisir les valeurs dans le terminal, au fur et à mesure, de la configuration du script, en réponse à une interaction avec l'utilisateur, sous-forme de questions. Pour cela, il suffira de saisir dans le terminal la valeur souhaitée et de faire « entrer ».

Les paramètres que nous retrouvons pour notre script_config_dhcp_dns.py sont :
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
Notre script_config_dhcp_dns.py est accompagné d'un second fichier : res.ini. Ce second fichier doit se trouver impérativement dans le même répertoire que script_config_dhcp_dns.py. Dedans, il sera déclarer nos sous-réseaux de la façons suivante, en prenant exemple ici pour 2 sous-réseaux :
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
Si nous reprenons notre exemple pour 2 sous-réseaux, lors de l'exécution du mode argument de notre script, l'argument -r <nombre de sous-réseaux> sera donc -r 2.
  
## Contexte et scénario de notre projet OpenClassrooms

Nous disposons de trois salles informatiques : 
La salle Cacao  qui fait se compose de notre serveur d'administration de notre réseau faisant office de serveur DHCP et DNS. Se trouve dans cette salle notre modem Internet et un poste de travail.
La salle Abeille composée d'un ensemble de poste de travail administrés depuis Cacao.
La salle Baobab qui comme la salle Abeille est simplement composé d'un ensemble de poste de travail administrés depuis Cacao.

Notre infrastructure se compose d'un réseau principal « Cacao » en 192.168.10.0/24 et des sous-réseaux propres aux salles « Abeille » en 192.168.100.0/24 et « Baobab » en 192.168.101.0/24.

![image](https://user-images.githubusercontent.com/72630371/140648992-7f93148b-fcbc-4f9c-9b35-9d27138ee03c.png)

