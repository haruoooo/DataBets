const palavrasChave = ["apost", "aposta", "apostar", "fazer aposta", "bet"];
const API_BACKEND = "http://localhost:5000/clique";
const TEMPO_ATUALIZACAO_SALDO_MS = 1000;

function contemPalavraChave(texto) {
    return palavrasChave.some(p => texto.includes(p));
}

function buscarSaldo() {
    try {
        const kaizen = document.querySelector("kaizen-header");
        if (!kaizen?.shadowRoot) return null;

        const saldoEl = kaizen.shadowRoot.querySelector("div.tw-font-bold.tw-text-sem-color-text-absolute-white.tw-mr-xs.tw-whitespace-nowrap");
        return saldoEl?.innerText.trim() || null;
    } catch (erro) {
        console.error("[ERRO] Captura de saldo falhou:", erro);
        return null;
    }
}

window.addEventListener("load", () => {
    console.log("[INFO] Rastreador ativo em:", window.location.href);

    document.addEventListener("click", (e) => {
        const alvo = e.target.closest("button");
        if (!alvo) return;

        const texto = (alvo.innerText || "").toLowerCase();
        if (!contemPalavraChave(texto)) return;

        setTimeout(() => {
            const saldo = buscarSaldo();

            const evento = {
                Executado: "Aposta Feita",
                valorAposta: texto.trim(),
                SaldoAtt: saldo,
                url: window.location.href
            };

            fetch(API_BACKEND, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(evento)
            });

            console.log("[INFO] Evento registrado:", evento);
        }, TEMPO_ATUALIZACAO_SALDO_MS);
    });
});
