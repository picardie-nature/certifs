#!/usr/bin/python
# -*- coding: utf-8

import smtplib
import cairo
import csv
import sys
import subprocess

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def make_certificat(fond,texte,sortie):
	certificat_surface = cairo.ImageSurface.create_from_png(fond)

	certificat = cairo.Context(certificat_surface)

	certificat.select_font_face("Sans")
	certificat.set_font_size(80)
	certificat.set_source_rgb(8.0/255,53.0/255,108.0/255)

	xb,yb,w,h,xa,ya = certificat.text_extents(texte)
	certificat.move_to(certificat_surface.get_width()/2-w/2,600)
	certificat.show_text(texte)

	scale_f=2

	img_pat = cairo.SurfacePattern(certificat_surface)
	scaler = cairo.Matrix()
	scaler.scale(scale_f,scale_f)
	img_pat.set_matrix(scaler)
	img_pat.set_filter(cairo.FILTER_BEST)
	
	canvas = cairo.ImageSurface(cairo.FORMAT_ARGB32, certificat_surface.get_width()/scale_f, certificat_surface.get_height()/scale_f)
	ctx = cairo.Context(canvas)
	ctx.set_source(img_pat)
	ctx.paint()

	canvas.write_to_png(sortie)

def make_mail(image, email, ta,tb):
	msg = MIMEMultipart()
	msg['Subject'] = 'Votre certificat de parrainage'
	msg['From'] = "secretariat@picardie-nature.org"
	msg['To'] = email 
	
	subprocess.call('convert %s %s'%(image,image.replace('png','jpg')), shell=True)
	fp = open(image.replace('png','jpg'), 'rb')
	txt = MIMEText("""Bonjour %s %s

Nous vous remercions encore une fois pour votre soutien à nos actions !

Veuillez trouver ci-joint votre certificat de parrainage.

Vous en souhaitant bonne réception.
Toute l'équipe de Picardie Nature.

"""%(tb,ta),'plain','utf-8')

	img = MIMEImage(fp.read())
	img.add_header('content-disposition', 'attachment', filename='certificat.jpg')

	fp.close()
	msg.attach(txt)
	msg.attach(img)


	s = smtplib.SMTP('localhost')
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()



liste = csv.reader(open("liste.csv","r"))

p=0
for personne in liste:
	p+=1
	if p >= 1:
		print personne
		ta,tb,tc,td,image,mail = personne
		image = image.replace('jpg','png')
		txt = "%s %s %s %s"%(ta,tc,tb,td)
		image_f = "%d.png"%(p)
		make_certificat(image,txt,image_f)
		make_mail(image_f,mail,tb,tc)
