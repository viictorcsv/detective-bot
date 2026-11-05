CASOS = [
    {
        "id": 1,
        "titulo": "O Roubo no Museu",
        "descricao": (
            "Na madrugada anterior à inauguração de uma exposição, a pintura "
            "Estrela de Eldoria desapareceu do museu. As câmeras da galeria "
            "ficaram desligadas entre 02h10 e 02h15. Só três funcionários "
            "estavam no prédio, e todos afirmam ter permanecido em seus postos."
        ),
        "suspeitos": [
            "Arthur — segurança; afirma que ficou na portaria.",
            "Helena — restauradora; afirma que ficou no ateliê.",
            "Marcos — técnico de manutenção; afirma que ficou no depósito.",
        ],
        "pistas": [
            "A pintura aparece na galeria às 02h10 e já não está lá às 02h15. "
            "Os acessos externos permaneceram trancados, sem entradas ou saídas.",
            "As gravações independentes da portaria e do ateliê mostram Arthur "
            "e Helena nesses locais durante todo o intervalo do desaparecimento.",
            "O desligamento das câmeras exigia acionar um interruptor na sala "
            "de manutenção. O registro biométrico mostra Marcos entrando ali "
            "às 02h09, contrariando seu relato. A sala tem uma passagem para a galeria.",
        ],
        "culpado": 2,
        "solucao": (
            "Marcos retirou a pintura. O desaparecimento ocorreu entre 02h10 e "
            "02h15, sem acesso de pessoas de fora. As gravações confirmam que "
            "Arthur e Helena permaneceram longe da galeria. Marcos mentiu sobre "
            "ficar no depósito: entrou na sala que permitia desligar as câmeras "
            "e acessar a galeria. Ele era o único dos três com oportunidade de agir."
        ),
    },
    {
        "id": 2,
        "titulo": "O Mistério da Biblioteca",
        "descricao": (
            "Durante a Noite dos Inventores, um manuscrito raro foi trocado "
            "por uma reprodução na biblioteca de Eldoria. O original tinha "
            "um selo dourado em relevo; a cópia traz apenas a imagem impressa "
            "do selo. Três pessoas manusearam o volume, uma de cada vez, "
            "antes de a vitrine ser fechada."
        ),
        "suspeitos": [
            "Beatriz — pesquisadora; foi a segunda a manusear o volume, para fotografá-lo.",
            "Otávio — bibliotecário; foi o primeiro a manusear o volume, para catalogá-lo.",
            "Lia — organizadora; foi a terceira a manusear o volume, para colocá-lo na vitrine.",
        ],
        "pistas": [
            "O vídeo contínuo da mesa confirma a ordem: Otávio, Beatriz e Lia. "
            "Ninguém mais tocou no volume, e a vitrine permaneceu lacrada após Lia fechá-la.",
            "Ao entregar o volume a Beatriz, Otávio o abriu diante da câmera. "
            "A imagem mostra o selo dourado em relevo: naquele momento, era o original.",
            "Beatriz cobriu a mesa com seu anteparo fotográfico. Quando o retirou "
            "e entregou o volume aberto a Lia, o vídeo já mostrava o selo plano "
            "e impresso da reprodução.",
        ],
        "culpado": 0,
        "solucao": (
            "Beatriz fez a troca enquanto o anteparo escondia a mesa. Ela recebeu "
            "o original de Otávio e entregou a reprodução a Lia, como mostram os "
            "dois registros do selo. O vídeo confirma que ninguém mais tocou no "
            "volume nesse intervalo. A troca aconteceu enquanto ele estava "
            "exclusivamente com Beatriz."
        ),
    },
    {
        "id": 3,
        "titulo": "O Laboratório Trancado",
        "descricao": (
            "Minutos antes da feira de ciências, o protótipo de um minirrobô "
            "desapareceu do laboratório de Eldoria. A porta ficou trancada "
            "entre 17h e 17h10, as janelas estavam lacradas e ninguém ficou "
            "lá dentro. Três integrantes da equipe estavam nas salas vizinhas. "
            "Como o robô saiu?"
        ),
        "suspeitos": [
            "Nina — programadora; afirma que ficou na sala de apresentação.",
            "Caio — técnico; afirma que não usou o terminal da sala de testes.",
            "Ravi — monitor; afirma que ficou no corredor diante da porta.",
        ],
        "pistas": [
            "Uma foto registra o robô numa cápsula de transporte no laboratório às 17h. Às 17h10 ele sumiu, "
            "mas os sensores confirmam que porta e janelas não abriram. Um tubo "
            "de transporte de peças liga o laboratório à sala de testes e comporta o robô.",
            "O registro do tubo mostra o envio de uma cápsula às 17h06. O sistema "
            "só funciona pelo terminal físico da sala de testes, sem controle remoto. "
            "A cápsula foi encontrada ali com o robô escondido entre espumas.",
            "O vídeo da sala de testes mostra Caio sozinho no terminal às 17h06, "
            "acionando o transporte e recolhendo a cápsula. Nina e Ravi não entraram "
            "nessa sala durante o intervalo.",
        ],
        "culpado": 1,
        "solucao": (
            "Caio usou o tubo de transporte para retirar o robô sem abrir o "
            "laboratório. O registro marca o envio às 17h06, e o vídeo mostra "
            "Caio operando o único terminal capaz de acioná-lo. O robô estava "
            "na cápsula que ele recolheu. Seu relato de que não usou o terminal "
            "é desmentido pelas evidências; a porta trancada era uma distração."
        ),
    },
]
