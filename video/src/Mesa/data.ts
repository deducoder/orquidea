import { z } from "zod";

const tono = z.enum(["tomate", "rosa", "cobalto", "amarillo", "verde", "crema"]);
const icono = z.enum(["taza", "bolsa", "galleta", "ticket"]);

// Every on-screen text and figure lives here, editable in Remotion Studio.
export const mesaSchema = z.object({
  // Optional image (staticFile path or URL) that replaces the text wordmark.
  logo: z.string().optional(),
  // Optional audio track (staticFile path or URL). Rendered if set.
  audioSrc: z.string().optional(),
  marca: z.string(),
  problema: z.object({ lineas: z.array(z.string()) }),
  presentacion: z.object({ titulo: z.string(), lineas: z.array(z.string()) }),
  carta: z.object({
    titular: z.string(),
    etiqueta: z.string(),
    categorias: z.array(z.string()),
    productos: z.array(
      z.object({
        nombre: z.string(),
        precio: z.number(),
        tono,
        icono,
      }),
    ),
    dias: z.array(z.string()),
    diaElegido: z.number().int().min(0),
    carrito: z.string(),
  }),
  pago: z.object({
    lineas: z.array(z.string()),
    encabezado: z.string(),
    resumen: z.array(z.object({ nombre: z.string(), precio: z.number() })),
    total: z.string(),
    boton: z.string(),
    confirmado: z.string(),
  }),
  whatsapp: z.object({
    lineas: z.array(z.string()),
    pedido: z.string(),
    dia: z.string(),
    hora: z.string(),
    resumen: z.string(),
  }),
  cocina: z.object({
    lineas: z.array(z.string()),
    encabezado: z.string(),
    comandas: z.array(z.object({ id: z.string(), detalle: z.string() })),
    nuevo: z.string(),
    pagado: z.string(),
    listo: z.string(),
  }),
  aviso: z.object({
    lineas: z.array(z.string()),
    boton: z.string(),
    mensaje: z.string(),
    pedido: z.string(),
  }),
  admin: z.object({
    lineas: z.array(z.string()),
    productos: z.object({
      encabezado: z.string(),
      items: z.array(z.string()),
      alta: z.string(),
    }),
    horarios: z.object({
      encabezado: z.string(),
      dias: z.array(z.string()),
      rango: z.string(),
      cerrado: z.string(),
      diaCerrado: z.number().int().min(0),
    }),
    planificador: z.object({
      encabezado: z.string(),
      contadores: z.array(z.object({ etiqueta: z.string(), valor: z.number() })),
    }),
  }),
  interno: z.object({
    etiqueta: z.string(),
    lineas: z.array(z.string()),
    cliente: z.string(),
    mesa: z.string(),
    mesaSub: z.string(),
    pago: z.array(z.string()),
    personal: z.string(),
    personalSub: z.string(),
  }),
  cierre: z.object({ lineas: z.array(z.string()), contacto: z.string() }),
});

export type MesaProps = z.infer<typeof mesaSchema>;

export const defaultProps: MesaProps = {
  marca: "Mesa",
  problema: { lineas: ["Filas.", "Prisas.", "Cobros a mano."] },
  presentacion: {
    titulo: "Mesa.",
    lineas: ["Pide.", "Paga.", "Recoge."],
  },
  carta: {
    titular: "Elige.",
    etiqueta: "Escanea el QR de la mesa",
    categorias: ["Café", "Comida", "Dulce"],
    productos: [
      { nombre: "Latte", precio: 45, tono: "amarillo", icono: "taza" },
      { nombre: "Bagel", precio: 52, tono: "rosa", icono: "bolsa" },
      { nombre: "Galleta", precio: 28, tono: "verde", icono: "galleta" },
      { nombre: "Combo", precio: 79, tono: "cobalto", icono: "ticket" },
    ],
    dias: ["L", "M", "X", "J", "V"],
    diaElegido: 3,
    carrito: "Carrito",
  },
  pago: {
    lineas: ["Paga", "antes."],
    encabezado: "Tu pedido",
    resumen: [
      { nombre: "Latte", precio: 45 },
      { nombre: "Bagel", precio: 52 },
      { nombre: "Galleta", precio: 28 },
    ],
    total: "Total",
    boton: "Pagar con Mercado Pago",
    confirmado: "Pago confirmado",
  },
  whatsapp: {
    lineas: ["El detalle", "vive en Mesa,", "no en el chat."],
    pedido: "Pedido #A12",
    dia: "Jueves",
    hora: "13:30",
    resumen: "1 Latte · 1 Bagel · 1 Galleta",
  },
  cocina: {
    lineas: ["Comandas", "en vivo."],
    encabezado: "Comandas",
    comandas: [
      { id: "#A12", detalle: "Latte · Bagel · Galleta" },
      { id: "#A13", detalle: "2 Latte" },
      { id: "#A14", detalle: "Combo" },
    ],
    nuevo: "Nuevo",
    pagado: "Pagado",
    listo: "Listo",
  },
  aviso: {
    lineas: ["El mensaje", "se arma solo."],
    boton: "Avisar",
    mensaje: "Tu pedido #A12 está listo",
    pedido: "#A12",
  },
  admin: {
    lineas: ["Tú", "mandas."],
    productos: {
      encabezado: "Productos",
      items: ["Latte", "Bagel", "Galleta", "Combo"],
      alta: "Nuevo",
    },
    horarios: {
      encabezado: "Horarios",
      dias: ["Lun", "Mar", "Mié", "Jue", "Vie"],
      rango: "8–16",
      cerrado: "Cerrado",
      diaCerrado: 2,
    },
    planificador: {
      encabezado: "Hoy",
      contadores: [
        { etiqueta: "Pedidos", valor: 24 },
        { etiqueta: "Por preparar", valor: 9 },
        { etiqueta: "Listos", valor: 15 },
      ],
    },
  },
  interno: {
    etiqueta: "Por dentro",
    lineas: ["Sin inventario.", "Sin historial de ventas."],
    cliente: "Cliente",
    mesa: "Mesa",
    mesaSub: "Supabase",
    pago: ["Mercado", "Pago"],
    personal: "Personal",
    personalSub: "comandas",
  },
  cierre: {
    lineas: ["Tu pedido,", "antes de llegar."],
    contacto: "hola@mesa.mx",
  },
};
