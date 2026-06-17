import codecs

html = codecs.open(r'c:\dixsys\manual_pjev\sitio_web\02_presupuesto\02.2.8-autorizacion-reserva.html', 'r', 'utf-8').read()
idx = html.find('id="module-process-table"')
if idx != -1:
    print(html[idx-100:idx+500].encode('ascii', 'replace').decode('ascii'))
