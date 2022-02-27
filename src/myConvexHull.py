def scoreChecker(el1, el2, el3):
    # Penggunaan determinan matriks untuk mengecek posisi titik dari garis yang melewati dua titik
    x1 = el1[0]
    y1 = el1[1]
    x2 = el2[0]
    y2 = el2[1]
    x3 = el3[0]
    y3 = el3[1]
    return x1*y2 + x3*y1 + x2*y3 - x3*y2 - x2*y1 - x1*y3

def distance(l1, l2, p):
    # Algoritma penghitungan jarak titik terhadap garis
    return abs(((l2[0]-l1[0])*(l1[1]-p[1])) - ((l1[0]-p[0])*(l2[1]-l1[1]))) / (((l2[0]-l1[0])**2 + (l2[1]-l1[1])**2)**0.5)

def triangleArea(p1, p2, p3):
    # Rumus luas segitiga
    return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2.0)

def inside(p1,p2,p3,p):
    # Mengecek apakah titik p berada di dalam segitiga yang dibentuk oleh titik p1, p2, p3
    a = triangleArea(p1,p2,p3)
    a1 = triangleArea(p,p2,p3)
    a2 = triangleArea(p1,p,p3)
    a3 = triangleArea(p1,p2,p)

    if(a == a1 + a2 + a3):
        return True
    else:
        return False

def subConvexHull(point, idxleft, idxright, array, subarr):
    # Perhitungan Sub Convex Hull
    idxMax = subarr[0]
    distleftMax = distance(array[idxleft], array[idxright], array[idxMax])

    for i in range(len(subarr)):
        if(distance(array[idxleft], array[idxright], array[subarr[i]]) > distleftMax):
            idxMax = subarr[i]
            distleftMax = distance(array[idxleft], array[idxright], array[idxMax])

    if [idxleft, idxright] in point:
        point.remove([idxleft, idxright])
    point.append([idxleft, idxMax])
    point.append([idxMax, idxright])

    subarr.remove(idxMax)

    for item in subarr:
        if(inside(array[idxleft], array[idxright], array[idxMax], array[item])):
            subarr.remove(item)

    outLeft = []
    outRight = []

    for i in range(len(subarr)):
        scoreLeft = scoreChecker(array[idxleft], array[idxMax], array[subarr[i]])
        scoreRight = scoreChecker(array[idxMax], array[idxright], array[subarr[i]])
        if(scoreLeft > 0):
            outLeft.append(subarr[i])
        
        if(scoreRight > 0):
            outRight.append(subarr[i])
    
    if len(outLeft)>0:
        subConvexHull(point, idxleft, idxMax, array, outLeft)
    
    if len(outRight)>0:
        subConvexHull(point, idxMax, idxright, array, outRight)

def myConvexHull(array):
    # Pembuatan array untuk menyimpan himpunan titik
    point = []
    
    # Cari titik paling kiri dan kanan sebagai garis pembagi
    idxleft = 0
    idxright = 0
    for i in range(len(array)):
        if(array[i][0] < array[idxleft][0]):
            idxleft = i
        if(array[i][0] > array[idxright][0]):
            idxright = i
    point.append([idxleft, idxright])

    # Penggolongan posisi titik terhadap garis pembagi
    arrLeft = []
    arrRight = []
    for i in range(len(array)):
        if(i != idxleft and i != idxright):
            score = scoreChecker(array[idxleft], array[idxright], array[i])
            if(score>0):
                arrLeft.append(i)
            elif(score<0):
                arrRight.append(i)

    # Pencarian sub convex hull untuk sisi kiri
    if len(arrLeft)>0:
        subConvexHull(point, idxleft, idxright, array, arrLeft)
    
    # Pencarian sub convex hull untuk sisi kanan
    if len(arrRight)>0:
        subConvexHull(point, idxright, idxleft, array, arrRight)

    return point