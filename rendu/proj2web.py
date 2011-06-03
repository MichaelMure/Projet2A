#! /usr/bin/env python
# -*- coding: utf_8 -*-

# Python 2.5.4 (r254:67916, Jan  8 2009, 14:20:40)

import commands
import chardet
import getopt, sys
import os, re
import chardet
import shutil

def usage():
	print 'Usage :',os.path.basename(sys.argv[0]),'[options] NUM'
	print """
	Toutes les ressources nécessaire au projet doivent être rassemblées 
	dans un répertoire unique nommé Projet_## où ## est le numéro du 
	projet dans la liste de référence (sur 2 chiffres de 01 à MAX), 
	directement sous la racine du site (cf. Arborescence).
	
	Options
	-h, --help:
		affiche ce message d'aide
	-f, --force_encodage
		force la détection de l'encodage du source sans tenir compte de 
		la borne <ENCODAGE>
	-r rep, --repertoire=rep
		définit rep comme le répertoire racine de l'arborescence cible 
		du site, le répertoire courant par défaut.
		
	Arborescence
		Toutes les ressources du site sont rassemblées sous une racine 
		unique (cf. option -r).
		À partir de cette racine, on trouvera :
		- les répertoires Projet_## (*) contenant chacun le matériel source
		  d'un projet : la page de description source nommée Projet_##.txt,
		  le poster original nommé Poster_##.pdf et les fichiers 
		  d'illustrations. 
		- Un seul répertoire «Posters» (**) où seront recopiés les pdf des 
		  posters originaux sous le nom Poster_##.pdf
		- les fichiers projet_##.html (**) qui contiendront la page html 
		  propre à chaque projet
		- les répertoires projet_##_fichiers (**) qui contiendront les 
		  ressources nécessaires aux pages html des projets (images, 
		  réduction des posters …)
		- le fichier index.html (**), page principale du site.
		
		(*) Fourni par l'utilisateur
		(**) Créé et mis à jour par le script
	"""
	sys.exit()
	
def arguments():
	try:
		opts,args=getopt.getopt(sys.argv[1:],'fhr:', ['help','racine='])
	except getopt.GetoptError, err:
		print str(err)
		usage()
	racine='.'
	force=False
	for opt,arg in opts:
		if opt in ('-h','--help'):
			usage()
		elif opt in ('-r','--racine'):
			racine=arg
		elif opt in ('-f','--force_encodage'):
			force=True
	if len(args) != 1:
		usage()
	else:
		try:
			num=int(args[0])
		except ValueError:
			print 'Erreur : Argument numérique entier positif !\n'
			usage()
	return(racine,num,force)

def get_encodage(page,force):
	pattern=r'<encodage>(.*?)</encodage>'
	regexp=re.compile(pattern,re.IGNORECASE | re.DOTALL)
	m=regexp.search(page)
	if not m or force:
		print 'Borne <encodage> absente ou détection forcée !'
		cd=chardet.detect(page)
		if cd['confidence'] >0.5:
		#if cd['confidence'] >0.8:
			code=cd['encoding']
		else:
			print 'Encodage trop incertain (%f)!' % cd['confidence']
			sys.exit(1)
	else:		
		code=m.group(1)
	return(code)

def copy_poster(fic):
	"""Assure la copie du poster dans le répertoire de regroupement des posters"""
	global racine
	dest=racine+'/Posters'
	if not os.path.isdir(dest):
		os.mkdir(dest)
	try:
		shutil.copy(fic,dest)
	except:
		print 'Erreur: Copie %s !\n' % fic

def verif_path(r,n):
	"""Vérifie l'existence de la racine et des éléments sources 
	   nécessaires au projet"""
	projet=r+'/Projet_%02u' % n
	poster=projet+'/Poster_%02u.pdf' % n
	if not os.path.isdir(r):
		print 'Erreur : répertoire racine invalide !\n'
		usage()
	else:
		if not os.path.isfile(poster):
			print 'Erreur : poster introuvable !\n'
			usage()
		elif not os.path.isfile(projet+'/Projet_%02u.txt' % n):
			copy_poster(poster)
			print 'Erreur : source HTML introuvable !\n'
			usage()
	copy_poster(poster)
	try:
		fsrc=open(projet+'/Projet_%02u.txt' % n,'r')
	except:
		print 'Erreur : ouverture fichier source en lecture !\n'
		sys.exit(2)
	try:
		fdst=open(r+'/Projet_%02u.html' % n,'w')
	except:
		print 'Erreur : ouverture fichier html en écriture !\n'
		sys.exit(2)
	return(projet,fsrc,fdst)

def get_head(titre):
	head="""
	<?xml version="1.0"?>
	<!DOCTYPE html 
		PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
		"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<!-- descriptions et inclusions -->
		<title>"""+titre+"""</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<meta http-equiv="Content-Language" content="fr" />
		<meta http-equiv="Content-Style-Type" content="text/css">
		<link rel="stylesheet" href="./style.css" type="text/css">
	</head>
	<body>
		<div class="topBanner">
			<table width="100%" cellpadding="4" cellspacing="0" border="0">
			<tr><td>
			<big><b><a href="http://www.ensisa.uha.fr/">ENSISA</a></b></big>
			</td>
			<td align="center"><big><b>
	  		<a href="./index.html">PROJETS 2<sup>e</sup> ANNÉE</a>
			</b></big></td>
			<td align="right"><big>
			<b><a href="http://www.uha.fr/">UHA</a></b>
			</big></td>
			</tr>
			</table>
		</div>
		<div class="leTitre">
    		<h1>"""+titre+"""</h1>
  		</div>
	"""
	return(head)
		
def write_entete(fic,texte):
	"""Entête de la page HTML du projet"""
	m=re.compile('<titre>(.*?)</titre>',re.IGNORECASE).search(texte)
	if m:
		titre=m.group(1)
	else:
		titre='Titre invalide !'
		print 'Titre invalide'
	fic.write(get_head(titre))
	return(titre)

def write_auteurs(fic,texte):
	"""Élèves et enseignants du projet"""
	fdst.write("""
		<div class="lesAuteurs">
		<h2>1 Auteur(s)</h2>
		<ul>
		<li><h4>Élève(s)</h4></li>
		<ul>""")
	n=0
	for elt in re.compile('<eleve>(.*?)</eleve>', \
	  re.IGNORECASE).finditer(texte):
		fdst.write('<li>'+elt.group(1)+'</li>\n')
		n+=1
	for elt in re.compile('<etudiant>(.*?)</etudiant>', \
		re.IGNORECASE).finditer(texte):
		fdst.write('<li>'+elt.group(1)+'</li>\n')
		n+=1
	if n==0:
		print 'Élèves invalides !'
	fdst.write("""
		</ul>
		<li><h4>Enseignant(s)</h4></li>
		<ul>""")
	for elt in re.compile('<enseignant>(.*?)</enseignant>', \
		re.IGNORECASE).finditer(texte):
		fdst.write('<li>'+elt.group(1)+'</li>\n')
		n+=1
	if n==0:
		print 'Enseignants invalides !'
	fic.write('</ul>\n</ul>\n')

def write_clefs(fic,texte):
	"""Mots clefs"""
	fdst.write("""
		<div class="lesMotsClefs">
		<h2>2 Mots clefs</h2>
		""")
	s=re.compile('<cle>(.*?)</cle>',re.IGNORECASE | re.DOTALL).search(texte)
	if s:
		fdst.write(s.group(1))
	else:
		print 'Mots clefs invalides'
	fdst.write('</div>\n')

def write_sujet(fic,texte):
	"""Présentation du sujet"""
	fdst.write("""
		<div class="leSujet">
		<h2>3 Sujet</h2>
		""")
	s=re.compile('<sujet>(.*?)</sujet>',re.IGNORECASE | re.DOTALL).search(texte)
	if s:
		fdst.write(s.group(1))
	else:
		print 'Sujet invalide'
	fdst.write('</div>\n')

def copy_file(fic,num):
	"""Transfert le fichier image voulu"""
	global racine
	org='%s/Projet_%02u/%s' %(racine,num,fic)
	dest='%s/Projet_%02u_fichiers' %(racine,num)
	if not os.path.isdir(dest):
		os.mkdir(dest)
	try:
		shutil.copy(org,dest)
	except:
		print 'Erreur: Copie %s !\n' % fic
	
def write_fig(fig,num):
	"""Renvoie le code html en place d'une figure"""
	fic=re.compile('<fichier>(.*?)</fichier>', \
		re.IGNORECASE | re.DOTALL).search(fig)
	leg=re.compile('<legende>(.*?)</legende>', \
		re.IGNORECASE | re.DOTALL).search(fig)
	if fic:
		ref='./Projet_%02u_fichiers/%s' % (num,fic.group(1))
		copy_file(fic.group(1),num)
		return("""
			<div class="figure_c">""" + \
				'<p><a href="'+ ref +'">' + \
				'<img class="scaled" src="' + ref +'">' + \
				'</a><p>' + leg.group(1) + \
			'</div>')
	else:
		print 'Image invalide !\n'
		return('<br>Image Invalide !<br>')
	
def write_realisation(fic,texte,num):
	"""Dévelopement"""
	fdst.write("""
		<div class="leDeveloppement">
		<h2>4 Réalisation</h2>
		""")
	s=re.compile('<realisation>(.*?)</realisation>', \
		re.IGNORECASE | re.DOTALL).search(texte)
	if s:
		par=s.group(1)
		par=par.replace('\n','<br>\n')
		par=par.replace('<br>\n<','\n<')
		rexp=re.compile('(<figure>(.*?)</figure>)',re.IGNORECASE | re.DOTALL)
		for fig in rexp.finditer(par):
			par=rexp.sub(write_fig(fig.group(1),num),par,1)
		fdst.write(par)
	else:
		print 'Réalisation invalide'
	fdst.write('</div>\n')

def write_contacts(fic,texte):
	"""Adresses courriels"""
	fdst.write("""
		<div class="leContact">
		<h2>5 Contact(s)</h2>""")
	n=0
	for elt in re.compile('<contact>(.*?)</contact>', \
		re.IGNORECASE).finditer(texte):
		fdst.write('<h6><a href=\"mailto:'+elt.group(1)+ \
			'">Renseignements complémentaires</a></h6>\n')
		n+=1
	if n==0:
		print 'Contacts invalides !'
	fdst.write('</div>\n')

def write_poster(fdst,num):
	"""Intègre une réduction à 25% du poster dans la page html"""
	global racine
	#reduc='%s/Projet_%02u_fichiers/Poster_%02u_a4.jpg' %(racine,num,num)
	href='./Projet_%02u_fichiers/Poster_%02u_a4.jpg' %(num,num)
	reduc='%s/%s' %(racine,href)
	if not os.path.isfile(reduc):
		poster='%s/Projet_%02u/Poster_%02u.pdf' %(racine,num,num)
		if not os.path.isfile(poster):
			print 'Erreur: Poster',poster,' absent !\n'
			return()
		else:
			#print 'convert -geometry 25%',poster,reduc
			u=commands.getoutput('convert -geometry 25%% %s %s' % \
			  (poster,reduc))
			if u:
				print 'Réduction du poster …',u
	if os.path.isfile(reduc):
		fdst.write("""
			<div class=\"lePoster\">
				<h1>Poster du projet</h1>
			</div>
			<div class="figure_c">""" + \
				'<p><a href="'+href+'">' + \
				'<img class="scaled" src="'+href+'">' + \
				"""</a><p>Réduction A4 du poster
			</div>""")

def write_end(fic):
	"""Ferme les bornes body et html"""
	fic.write("""
	</body>
	</html>""")

def write_index(num,titre):
	global racine
	nom=racine+'/index.html'
	if os.path.isfile(nom):
		fic=open(nom,'r')
		texte=fic.read()
		fic.close()
		rexp=re.compile('(<li>Projet %u :.*?</li>)' % num,re.IGNORECASE | re.DOTALL)
		if rexp.search(texte):
			texte=rexp.sub('<li>Projet %u : <a href="./Projet_%02u.html">%s</a></li>\n'  \
			% (num,num,titre),texte)
		else:
			max=0
			for s in re.compile('<li>Projet (\d+).*?</li>', \
			  re.IGNORECASE | re.DOTALL).finditer(texte):
				if int(s.group(1)) > max:
					max=int(s.group(1))
			for i in range (max+1,num):
				texte += '<li>Projet %u : Invalide</li>\n' % i
			texte += '<li>Projet %u : <a href="./Projet_%02u.html">%s</a></li>\n' \
		  	  % (num,num,titre)
		fic=open(nom,'w')
		fic.write(texte)
		fic.close()
	else:
		fic=open(nom,'w')
		fic.write(get_head('Liste des projets')+'\n<ul>')
		for i in range (1,num):
			fic.write('<li>Projet %u : Invalide</li>\n' % i)
		fic.write('<li>Projet %u : <a href="./Projet_%02u.html">%s</a></li>\n' \
		  % (num,num,titre))
		fic.close()

global racine
(racine,num,force)=arguments()
(rep,fsrc,fdst)=verif_path(racine,num)
texte=fsrc.read()
code=get_encodage(texte,force)
print 'Encodage :',code
if not re.compile('utf.*8',re.IGNORECASE).match(code):
	print 'Encodage UTF-8 nécessaire'
	try:
		texte=texte.decode(code).encode('utf-8')
	except:
		print 'Décodage/encodage UTF-8 impossible !\n'
		sys.exit(2)
titre=write_entete(fdst,texte)
write_auteurs(fdst,texte)
write_clefs(fdst,texte)
write_sujet(fdst,texte)
write_realisation(fdst,texte,num)
write_contacts(fdst,texte)
write_poster(fdst,num)
write_end(fdst)
fsrc.close()
fdst.close()
write_index(num,titre)





