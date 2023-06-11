"""Обозначения Байера. Буква характеризует яркость звезды. Аlp - самая яркая, Bet - менее яркая и тд """

EN_NAMES = ['', 'Alp', 'Bet', 'Chi', 'Del', 'Eps', 'Eta', 'Gam', 'Iot', 'Kap', 'Lam', 'Mu', 'Nu', 'Ome', 'Omi', 'Phi',
            'Pi', 'Psi', 'Rho', 'Sig', 'Tau', 'The', 'Ups', 'Xi', 'Zet']
LAT_NAMES = ['', 'α', 'β', 'χ', 'δ', 'ε', 'η', 'ɣ', 'ɩ', 'ϰ', 'λ', 'μ', 'ν', 'ω', 'ο', 'ϕ', 'π', 'ψ', 'ϱ', 'σ', 'τ',
             'ϑ', 'Ʊ', 'ξ', 'ζ']
EN2LAT_MAP = {EN_NAMES[i]: LAT_NAMES[i] for i in range(0, len(EN_NAMES))}
