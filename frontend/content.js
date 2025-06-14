const palavrasChave = ["apost", "aposta", "apostar", "fazer aposta", "bet"];
const API_BACKEND = "http://localhost:5000/clique";
const TEMPO_ATUALIZACAO_SALDO_MS = 2000;

function contemPalavraChave(texto) {
    return palavrasChave.some(p => texto.includes(p));
}

window.addEventListener("load", () => {
    console.log("[INFO] Rastreador ativo em:", window.location.href);

    document.addEventListener("click", (e) => {
        const alvo = e.target.closest("button");
        if (!alvo) return;

        const texto = (alvo.innerText || "").toLowerCase();
        if (!contemPalavraChave(texto)) return;

        setTimeout(() => {
            const oddEl = document.querySelector('[data-qa="bet-odds-value"]');
            const odd = oddEl ? parseFloat(oddEl.innerText.replace(",", ".").trim()) : null;

            const timeEl = document.querySelector('[data-qa="selection-label"]');
            const time = timeEl ? timeEl.innerText.trim() : null;

            const valor = texto.trim();

            const evento = {
                time: time,
                valor_aposta: parseFloat(valor.replace(/[^\d,.-]/g, "").replace(",", ".")) || null,
                odd: odd
            };

            fetch(API_BACKEND, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(evento)
            })
            .then(response => response.json())
            .then(data => {
                if (data.alerta === true) {
                    alert("ALERTA: Cuidado, está arriscando-se DEMAIS!");
                }
            })
            .catch(err => {
                console.error("[ERRO] Falha ao enviar dados para o backend:", err);
            });

            console.log("[INFO] Evento enviado ao backend:", evento);
        }, TEMPO_ATUALIZACAO_SALDO_MS);
    });
});
