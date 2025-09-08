// ✅ Opção A — simples (se já tem middleware protegendo rotas)
import { redirect } from "next/navigation";

export default function Home() {
  // manda a home direto para a lista de pedidos
  redirect("/pedidos");
}
