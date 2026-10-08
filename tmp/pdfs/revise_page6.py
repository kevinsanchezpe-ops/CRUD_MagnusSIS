from io import BytesIO
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.utils import simpleSplit
from pathlib import Path
W,H=792,612; b=BytesIO(); c=canvas.Canvas(b,pagesize=(W,H)); ink=HexColor('#222222'); gray=HexColor('#dedede'); line=HexColor('#333333'); muted=HexColor('#555555')
def wrapped(text,x,top,width,size=8,leading=10,bold=False):
 f='Helvetica-Bold' if bold else 'Helvetica'; c.setFillColor(ink); c.setFont(f,size)
 for j,s in enumerate(simpleSplit(text,f,size,width)): c.drawString(x,top-j*leading,s)
c.setFillColor(ink); c.setFont('Helvetica-Bold',12); c.drawString(40,565,'Detalle de actores y acciones')
x=40; top=546; a=112; d=600; hh=20
c.setStrokeColor(line); c.setLineWidth(.7)
for xx,ww in [(x,a),(x+a,d)]: c.setFillColor(gray); c.rect(xx,top-hh,ww,hh,fill=1,stroke=1)
c.setFillColor(ink); c.setFont('Helvetica-Bold',8.5); c.drawString(x+6,top-13,'Actor'); c.drawString(x+a+6,top-13,'Acciones que puede ejecutar')
y=top-hh
for label,desc,rh in [('Usuario','Registrar, consultar, buscar, actualizar y eliminar productos; consultar y gestionar categorías.',27),('Administrador','Realizar las mismas operaciones del Usuario y administrar información desde el panel administrativo de Django.',33)]:
 c.setFillColor(white); c.rect(x,y-rh,a,rh,fill=1,stroke=1); c.rect(x+a,y-rh,d,rh,fill=1,stroke=1); c.setFillColor(ink); c.setFont('Helvetica',8.2); c.drawString(x+6,y-rh/2-3,label); wrapped(desc,x+a+6,y-10,d-12,8,9.5); y-=rh
wrapped('Límite del sistema: las funciones anteriores pertenecen al sistema de inventario; el panel Django es acceso administrativo. Las asociaciones son simples, sin include ni extend. Los actores y permisos son conceptuales: la autenticación aún no está implementada.',40,455,710,7.6,9.5)
c.setFont('Helvetica-Bold',12); c.drawString(40,386,'1.4 Diagrama de clases (UML)')
def class_box(x,y,w,h,title,attrs,methods):
 c.setStrokeColor(ink); c.setLineWidth(1); c.setFillColor(white); c.rect(x,y,w,h,fill=1,stroke=1); header=25; ah=len(attrs)*14+8
 c.setFillColor(gray); c.rect(x,y+h-header,w,header,fill=1,stroke=1); c.setFillColor(ink); c.setFont('Helvetica-Bold',10); c.drawCentredString(x+w/2,y+h-17,title); c.setFont('Helvetica',8.1)
 yy=y+h-header-14
 for q in attrs: c.drawString(x+9,yy,q); yy-=14
 divider=y+h-header-ah; c.line(x,divider,x+w,divider); yy=divider-13
 for q in methods: c.drawString(x+9,yy,q); yy-=14
class_box(50,240,235,140,'Categoria',['- id : int','- nombre : String','- descripcion : String'],['+ crear() : void','+ actualizar() : void','+ eliminar() : void','+ obtenerProductos() : List<Producto>'])
class_box(430,155,320,225,'Producto',['- id : int','- nombre : String','- descripcion : String','- categoria : Categoria','- precio : Decimal','- cantidad : int','- fecha_creacion : DateTime','- fecha_actualizacion : DateTime'],['+ crear() : void','+ actualizar() : void','+ eliminar() : void','+ validarDatos() : boolean','+ buscar(termino : String) : List<Producto>'])
c.setStrokeColor(ink); c.setLineWidth(.8); c.line(285,310,430,310); c.setFillColor(ink); c.setFont('Helvetica-Bold',8); c.drawString(292,317,'1'); c.drawString(407,317,'0..*'); c.setFont('Helvetica',7.5); c.drawCentredString(357,297,'contiene')
wrapped('Figura 4. Clases Categoria y Producto con atributos tipados (-), métodos (+) y cardinalidad 1 a 0..*.',40,137,710,7.5,9)
wrapped('Relación: una categoría tiene cero o muchos productos; cada producto pertenece a una sola categoría. El modelo es simple y no requiere herencia ni composición. Los métodos se muestran como stubs propuestos, en coherencia con el apartado 3.3.',40,119,710,7.5,9)
c.setStrokeColor(HexColor('#cccccc')); c.line(40,33,752,33); c.setFillColor(muted); c.setFont('Helvetica',7); c.drawString(40,20,'Sistema Web de Gestión de Inventario'); c.drawRightString(752,20,'Página 6'); c.save(); b.seek(0); pg=PdfReader(b).pages[0]
r=PdfReader('documento_Sistema.pdf'); w=PdfWriter()
for i,p in enumerate(r.pages): w.add_page(pg if i==5 else p)
out=Path('tmp/pdfs/documento_Sistema_diseno_original.pdf')
with out.open('wb') as f:w.write(f)

