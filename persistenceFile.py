import sys
import math
import os
import numpy as np
from fpdf import FPDF
import matplotlib.pyplot as plt

nombreDatos= [  'Glucosa Media', 'Desviacion tipica','Glucosa maxima media',
                'Glucosa minima media','Porcentaje de tiempo en rango 70-180',
                'Numero medio de eventos por debajo del minimo(60)',
                'Numero medio de eventos por encima del maximo (240)',
                'Maximo numero de eventos fuera de rango(60-240)',
                'Minimo numero de eventos fuera de rango(60-240)']

def getPlotAndSave(clusters,ruta):
    n_clusters=len(clusters)
    for i in range(n_clusters):
        for group in clusters[i]:
            if (n_clusters<4):
                plt.subplot(1,3,i+1)
            elif (n_clusters<5):
                plt.subplot(2,2,i+1)
            elif (n_clusters<7):
                plt.subplot(2,3,i+1)
            elif(n_clusters<9):
                plt.subplot(2,4,i+1)
            elif(n_clusters==9):
                plt.subplot(3,3,i+1)
            elif(n_clusters==10):
                plt.subplot(2,5,i+1)
            elif(n_clusters<=16):
                plt.subplot(4,4,i+1)
            elif(n_clusters<=25):
                plt.subplot(5,5,i+1)
            elif(n_clusters<=36):
                plt.subplot(6,6,i+1)
            plt.plot(group)
            plt.axis([0,15,40,350])
    plt.savefig(ruta+'img.png')
    #plt.show()
    #return plt

def genParam(clusters,metodo):
    n=0
    tra=0
    for tramos in clusters:
        n+=1
        for tramo in tramos:
            tra+=1
    param=""
    param+="En este caso se ha optado por la tecnica de clustering conocida como "
    param+=metodo
    param+=", tras haber identificado hasta "
    param+=str(tra)
    param+=" tramos validos y completos, los hemos asociado en "
    param+=str(n)
    param+=" grupos, llamados clusters de ahora en adelante."
    return param

def genDescGraf(codes):
    frase=""
    letra='a'
    for cluster,nCluster in zip(codes,range(len(codes))):
        frase+="El cluster numero "+ str(nCluster+1)+" esta formado por "
        salto=False
        for tramo, nTramo in zip(cluster,range(len(cluster))):
            if(tramo>0):
                salto=True;
                if(tramo==1):
                    frase+= "1 tramo correspodiente "
                elif(tramo>1):
                    frase+= str(tramo)+" tramos correspondientes "
                frase+="a las horas entre "
                if(nTramo==0):
                    frase+="medianoche y las 4 am, "
                elif(nTramo==1):
                    frase+="las 4 am y las 8 am, "
                elif(nTramo==2):
                    frase+="las 8 am y mediodia, "
                elif(nTramo==3):
                    frase+="mediodia y las 4 pm, "
                elif(nTramo==4):
                    frase+="las 4 pm y las 8 pm, "
                elif(nTramo==5):
                    frase+="las 8 pm y medianoche."
        if (salto):
            frase+='\n'
    return frase

def getInfo(clusters):
    datos=[]
    for i in range(len(clusters)):
        datos.append([])
        for j in range(9):
            datos[i].append([])
    for i in range(len(clusters)):
        sumaDeMedias=0
        sumaDeMaximos=0
        sumaDeMinimos=0
        sumaDeEventosBajos=0
        sumaDeEventosAltos=0
        nSegmentos=0
        n=0
        glucosaMinMedia=sys.maxint
        glucosaMaxMedia=0
        nVecesEnRango=0
        nMinDeEventosMalos=16
        nMaxDeEventosMalos=0
        sumaDeEventosMalosGrupo=0
        for group in clusters[i]:
            sumaDeMedias+=group.mean()
            sumaDeMaximos+=group.max()
            sumaDeMinimos+=group.min()
            nSegmentos+=1
            for registro in group:
                n+=1
                if (registro>=70 and registro<=180):
                    nVecesEnRango+=1
                elif (registro<=60):
                    sumaDeEventosBajos+=1
                    sumaDeEventosMalosGrupo+=1
                elif (registro>=240):
                    sumaDeEventosAltos+=1
                    sumaDeEventosMalosGrupo+=1
            if(sumaDeEventosMalosGrupo>nMaxDeEventosMalos):
                nMaxDeEventosMalos=sumaDeEventosMalosGrupo
            elif(sumaDeEventosMalosGrupo<nMinDeEventosMalos):
                nMinDeEventosMalos=sumaDeEventosMalosGrupo
        datos[i][0]=sumaDeMedias/nSegmentos #media
        datos[i][2]=sumaDeMaximos/nSegmentos #media de maximos
        datos[i][3]=sumaDeMinimos/nSegmentos #media de minimos
        datos[i][4]=float(nVecesEnRango)/n*100 #% de tiempo en rango
        datos[i][5]=float(sumaDeEventosBajos)/n #media de eventos bajos <60
        datos[i][6]=float(sumaDeEventosAltos)/n #media de eventos altos >240
        datos[i][7]=nMaxDeEventosMalos #maximo de eventos malos en un mismo segmento
        datos[i][8]=nMinDeEventosMalos #minimo de eventos malos en un mismo segmento
        varianza=0
        n=0
        for group in clusters[i]:
            for registro in group:
                varianza+=(registro-datos[i][0]) ** 2
                n+=1
        varianza=varianza/n
        datos[i][1]=math.sqrt(varianza) #Desviacion estandar
    return datos

def genTabla(clusters,pdf):
    info=getInfo(clusters)
    pdf.cell(10,5,'','LTBR',0,'C',0)
    pdf.cell(20,5,'A',1,0,'C',0)
    pdf.cell(20,5,'B',1,0,'C',0)
    pdf.cell(20,5,'C',1,0,'C',0)
    pdf.cell(20,5,'D',1,0,'C',0)
    pdf.cell(20,5,'E',1,0,'C',0)
    pdf.cell(20,5,'F',1,0,'C',0)
    pdf.cell(20,5,'G',1,0,'C',0)
    pdf.cell(20,5,'H',1,0,'C',0)
    pdf.cell(20,5,'I',1,0,'C',0)
    pdf.ln()
    n=1
    for cluster in info:
        pdf.cell(10,5,str(n),1,0,'C',0)
        for dato,d in zip(cluster,range(len(cluster))):
            if (d<4 or d==5 or d==6):
                pdf.cell(20,5,str(round(dato,2)),1,0,'C',0)
            elif(d==4):
                pdf.cell(20,5,str(round(dato,2))+'%',1,0,'C',0)
            elif(d>=7):
                pdf.cell(20,5,str(int(dato)),1,0,'C',0)
        n+=1
        pdf.ln()
    return pdf

def saveData(ruta,etiquetas,nombres,datos):
    nCarpetas=etiquetas.max()
    for i in range(nCarpetas+1):
        os.mkdir(ruta+str(i))
    for cluster,nombre,dato in zip(etiquetas,nombres,datos):
        np.savetxt(ruta+str(cluster)+'/'+str(nombre),dato,fmt='%i',delimiter=" ")

def toPDF(clusters,codes,metodo,ruta=""):
    pdf=FPDF('P','mm','A4')
    pdf.add_page()
    titulo="Informe glucemico"
    w = len(titulo) + 6
    pdf.set_x((210 - w) / 2)
    pdf.set_font('Times','B',20)
    pdf.cell(w,9,titulo,0,1,'C',0)
    pdf.ln()
    pdf.set_font('Times','',12)
    with open('Introduccion', 'rb') as fh:
            intro = fh.read().decode('utf-8')
    pdf.multi_cell(0,5,intro)
    pdf.ln()
    param=genParam(clusters,metodo)
    pdf.multi_cell(0,5,param)
    with open('explica', 'rb') as fh:
            pos = fh.read().decode('utf-8')
    pdf.multi_cell(0,5,pos)
    getPlotAndSave(clusters,ruta)
    pdf.image(ruta+'img.png', 0,pdf.get_y() ,8*28)
    pdf.add_page()
    pdf.multi_cell(0,5,genDescGraf(codes))
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf=genTabla(clusters,pdf)
    pdf.add_page()
    with open('responsabilidad', 'rb') as fh:
            res = fh.read().decode('utf-8')
    pdf.multi_cell(0,5,res,border=1)
    pdf.output(ruta+'informe.pdf','F')