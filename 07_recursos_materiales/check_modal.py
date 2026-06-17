import codecs

html = codecs.open(r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.2.8-autorizacion-reserva.html', 'r', 'utf-8').read()
idx = html.find('Anexo 2:')
if idx != -1:
    print(html[max(0, idx-1000):idx+1000].encode('ascii', 'replace').decode('ascii'))
