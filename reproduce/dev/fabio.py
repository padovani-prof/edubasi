def mostrar_dados_iniciais(df):
    print('Quantidades de Analizados: ', len(df))
    print('Quantidades de alunos Regulares: ', len(df[df['IN_TREINEIRO'] == '0'])) 
    print('Quantidades de alunos Treineiros: ', len(df[df['IN_TREINEIRO'] == '1']))
    print('Quantidade de alunos de lingua estrageira (inglesa): ',len(df[df['TP_LINGUA'] == '0']))
    print('Quantidade de alunos de lingua estrageira (Espanhola): ',len(df[df['TP_LINGUA'] == '1']))

