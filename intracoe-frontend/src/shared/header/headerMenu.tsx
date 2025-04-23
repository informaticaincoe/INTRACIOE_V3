import { useState } from "react";
import defaultPerfil from "../../assets/grupo_incoe_logo.png"
import { PerfilMenu } from "./perfilMenu";

export const HeaderMenu = () => {
  const [visible, setVisible] = useState<boolean>(false);
  return (
    <nav className="bg-primary-blue sticky top-0 z-40 flex justify-between px-10 py-5">
      <h1 className="text-xl font-semibold">
        <span className="text-white">Intra</span>
        <span className="text-primary-yellow">coe</span>
      </h1>
      <span className="flex gap-2 hover:cursor-pointer hover:bg-[#384183] rounded-full px-4 py-1" onClick={() => setVisible(true)}>
        <img src={defaultPerfil} alt="perfil" className="object-cover h-7 rounded-full" />
        <p className="text-white">usuario</p>
      </span>
      <PerfilMenu visible={visible} setVisible={setVisible} />
    </nav>
  );
};
