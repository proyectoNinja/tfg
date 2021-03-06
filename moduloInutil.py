def HDBSCANclustering(data):
    clusterer = hdbscan.HDBSCAN(metric='euclidean',min_cluster_size=2, min_samples=2)
    clusterer.fit(data)
    _nClusters=clusterer.labels_.max()+1
    clusters=[]
    for i in range(_nClusters+1):
        clusters.append([])
    for i,j in zip(clusterer.labels_,data):
        if (i!=-1):
            clusters[i].append(j)
        else:
            clusters[_nClusters-1].append(j)
    return clusters


def get_codigoTramo(hora):
    tramo=0
    if (hora<4):
        tramo=0
    elif(hora<8):
        tramo=1
    elif(hora<12):
        tramo=2
    elif(hora<16):
        tramo=3
    elif(hora<20):
        tramo=4
    else:
        tramo=5
    return tramo

def gt_group(hora,hMin):
    format="%Y/%m/%d %H:%M"
    group = 0
    hora_Actual=datetime.strptime(hora,format)
    hora_minima=datetime.strptime(hMin,format)
    dia0=hora_minima.day
    mes0=hora_minima.month
    anyo0=hora_minima.year
    hora_base=datetime.strptime(anyo0+"/"+mes0+"/"+dia0,"%Y/%m/%d")
    print hora-hMin

def calculaPendiente(data):
    anterior=data['Historico'].mean()
    pendiente=[]
    for his in data['Historico']:
        pendiente.append(his-anterior)
        anterior=his
    data['Pendiente']=pendiente


def printAndPlotGroup(data,grupo):
    imprimir=data.get_group(grupo).drop('Grupo',axis=1)
    print imprimir
    imprimir.plot()
    plt.show()

def randomForestClustering(datas,normalizar):
    if (normalizar):
        data=norm().fit_transform(datas)
    else:
        data=datas
    print rfc
    cluster_labels=rfc.RandomForestEmbedding().fit_transform(data)
    print cluster_labels
    return cluster_labels

def clasificaPorHora(hora,hMin,format,desplazamiento):
    hClasificar=datetime.strptime(hora,format)
    hRef=datetime.strptime(hMin,format)
    grupo=desplazamiento*100
    clasificado=False
    while(not clasificado):
        horas=4*(grupo+1)
        if(hRef+timedelta(hours=horas)>hClasificar):
            clasificado=True
        else:
            grupo=grupo+1
    return int(grupo)

def filtro(data,tipo):
    if (tipo==0):
        col=['Historico','Hora','Grupo']
        data=data[col]
        data=data.dropna(axis=0)
    elif (tipo==1):
        col=['Leida','Hora','Grupo']
        data=data[col]
        data=data.dropna(axis=0)
    format="%Y/%m/%d %H:%M"
    data.set_index('Hora', inplace=True)
    return data

def spectral_Clustering(data):
    etiquetas=[]
    mejor=0
    numero=0
    for n_clusters in range(6):
        clusterer = spectral_clustering(data,n_clusters=n_clusters+5, random_state=10)
        cluster_labels = clusterer.fit_predict(data)
        valor = silhouette_score(data, cluster_labels)
        if (valor>mejor):
            mejor=valor
            etiquetas=cluster_labels
            numero=n_clusters+5
    clusters=[]
    for i in range(numero):
        clusters.append([])
    for i,j in zip(etiquetas,data):
        clusters[i].append(j)
    return clusters

def infoKMeans(data_trabajo, data_valores):
    for n_clusters in range(16):
        clusterer = KMeans(n_clusters=n_clusters+2, random_state=10)
        cluster_labels = clusterer.fit_predict(data_trabajo)
        silhouette_avg = silhouette_score(data_valores, cluster_labels)
        cal_score = calinski_harabaz_score(data_valores,cluster_labels)
        print("For n_clusters =", n_clusters+2,
              "The average silhouette_score is :", silhouette_avg,
              ", the calinski_harabaz score is ", cal_score,)

def main2():
    for param, index in zip(sys.argv,range(len(sys.argv))):
        if (index==1):
            data=getRegistros0(parser(param,index-1))
        elif(index>1):
            lectura=getRegistros0(parser(param,index-1))
            data=data.append(lectura)
    inOut=procesado(data,"nkmeans",nucleos=16)
