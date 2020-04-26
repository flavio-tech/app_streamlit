import streamlit as st
import pandas as pd
import altair as alt
import locale



def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart


def criar_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width = 600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars

def criar_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

def criar_scatterplot(x, y, color, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        color = color,
        tooltip = [x, y]
    ).interactive()
    return scatter

def cria_correlationplot(df, colunas_numericas):
    cor_data = (df[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    base = alt.Chart(cor_data, width=500, height=500).encode( x = 'variable2:O', y = 'variable:O')
    text = base.mark_text().encode(text = 'correlation_label',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
    alt.value('black')))

# The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
    color = 'correlation:Q')

    return cor_plot + text


def main():
    # tela principal com logo e motivação
    #st.image('https://hackernoon.com/drafts/f2px36fy.png', width = 450)
    st.image('hello_small.gif')
    st.header(' ')
      
    # Menu lateral
    st.sidebar.title('AceleraDev Data Science')
    st.sidebar.markdown('Powered by')
    st.sidebar.image('logo.png', width=200)
    st.sidebar.markdown(' ')
    st.sidebar.markdown(' ')
    st.sidebar.markdown(' ')
    st.sidebar.markdown(' ')
    st.sidebar.markdown("**Selecione a demo ou outro arquivo para analisado**")

    #selecione entre Demo ou seu arquivo para análise
    choice = st.sidebar.radio(
        '', 
        ('demo', 'vou importar um arquivo')
    )  
    for i in range(5):
        st.sidebar.markdown(' ')
    st.sidebar.title('Sugestões para (gmail):')
    st.sidebar.markdown('* flaviosilva250')
    
    
    if choice == 'demo':
        st.subheader('cortesia de')
        st.image('AngelList.png')
        file = 'companies_clean.csv'
        demo = True
    else:
        st.markdown('**no formato .csv**')
        file = st.file_uploader('', type = 'csv')
        demo = False
    if file is not None:
        st.header('**Exploratory Data Analysis**')
        st.markdown(' ')
        st.markdown(' ')
        df = pd.read_csv(file)
        st.markdown('**Número de linhas:**')
        st.markdown(df.shape[0])
        st.markdown(' ')
        st.markdown('**Número de colunas:**')
        st.markdown(df.shape[1])
        st.markdown(' ')
        st.markdown('**Visualizando o dataframe**')
        number = st.slider('Escolha o numero de linhas que deseja ver', min_value=1, max_value=20, value=6)
        st.dataframe(df.head(number))
        st.markdown('**Nome das colunas:**')
        st.markdown(list(df.columns))

        exploracao = pd.DataFrame({'nomes' : df.columns, 'tipos' : df.dtypes, 'NA #': df.isna().sum(), 'NA %' : (df.isna().sum() / df.shape[0]) * 100})
        st.markdown('**Tipos de dados**')
        st.write(exploracao)
        st.markdown(' ')
        st.markdown('**Contagem dos tipos de dados:**')
        st.write(exploracao.tipos.value_counts(dropna=False))

        # tratamento dos dados faltantes
        st.markdown('**Tabela com coluna e percentual de dados faltantes :**')
        st.table(exploracao[exploracao['NA #'] != 0][['tipos', 'NA %']])
        # se houver dados faltantes
        if df.isna().sum().any():
            st.markdown('**Quer eliminar as entradas com dados faltantes?**')
            select_method = st.radio('Escolha um metodo abaixo :', ('Sim', 'Não'))
            st.markdown('Você selecionou : ' +str(select_method))
            if select_method == 'Sim':
                df.dropna(axis=0, inplace=True)
                st.subheader("Observe o novo número de linhas e colunas")
                st.markdown('**Número de linhas:**')
                st.markdown(df.shape[0])
                st.markdown('**Número de colunas:**')
                st.markdown(df.shape[1])
            
            if select_method == 'Não':
                pass

        st.markdown(' ')
        st.markdown(' ')
        st.header('Estatística descritiva univariada')
        st.subheader('Nota: Algumas opções funcionam apenas para dados numéricos do dataframe')
        #st.image('https://imagens-voitto.s3.amazonaws.com/imagens-blog/meta/963b9ed4a8402803a51366d488f444b5.jpg', width = 400)
        st.image('stat_small.jpg')
        aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})
        colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
        colunas = list(df.columns)
        col = st.selectbox('Selecione a coluna :', colunas_numericas)
        if col is not None:
            st.markdown('Selecione o que deseja analisar :')
            mean = st.checkbox('Média')
            if mean:
                if demo:
                    locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
                    st.markdown(locale.currency(df[col].mean(), grouping=True))
                else:
                    st.markdown(df[col].mean())
            median = st.checkbox('Mediana')
            if median:
                if demo:
                    locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
                    st.markdown(locale.currency(df[col].median(), grouping=True))
                else:
                    st.markdown(df[col].median())
            desvio_pad = st.checkbox('Desvio padrão')
            if desvio_pad:
                st.markdown(df[col].std())
            kurtosis = st.checkbox('Kurtosis')
            if kurtosis:
                st.markdown(df[col].kurtosis())
            skewness = st.checkbox('Skewness')
            if skewness:
                st.markdown(df[col].skew())
            describe = st.checkbox('Describe')
            if describe:
                st.table(df[colunas_numericas].describe().transpose())
        st.header('Visualização dos dados')
        st.header(' ')
        #st.image('http://www.empowerbi.com.br/images/service-2.jpg', width=400)
        st.image('vis_small.jpg')
        st.markdown('Selecione a visualizacao')
        view = st.radio(
        'Selecione a visualizacao',      
        ('Histograma', 'Gráfico de barras', 'Boxplot', 'Scatterplot', 'Correlação')
    )  
        if view == 'Histograma':
            if demo:
                col_angel = st.selectbox('Selecione o estágio do investimento: ', df["Stage"].unique())
                st.markdown('Histograma dos investimentos ' + str(col_angel))
                df_col = df[df['Stage'] == col_angel]
                st.write(criar_histograma('Total Raised', df_col))
            else:
                col_num = st.selectbox('Selecione a Coluna Numerica: ', colunas_numericas,key = 'unique')
                st.markdown('Histograma da coluna : ' + str(col_num))
                st.write(criar_histograma(col_num, df))

        if view == 'Gráfico de barras':
            col_num_barras = st.selectbox('Selecione a coluna numerica: ', colunas_numericas, key = 'unique')
            col_cat_barras = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key = 'unique')
            st.markdown('Gráfico de barras da coluna ' + str(col_cat_barras) + ' pela coluna ' + col_num_barras)
            st.write(criar_barras(col_num_barras, col_cat_barras, df))

        if view == 'Boxplot':
            col_num_box = st.selectbox('Selecione a Coluna Numerica:', colunas_numericas,key = 'unique' )
            col_cat_box = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key = 'unique')
            st.markdown('Boxplot ' + str(col_cat_box) + ' pela coluna ' + col_num_box)
            st.write(criar_boxplot(col_num_box, col_cat_box, df))

        if view == 'Scatterplot':
            if demo:
                st.markdown("Nota: nesta versão ainda não temos suporte para scatterplot com colunas categóricas")
            col_num_x = st.selectbox('Selecione o valor de x ', colunas_numericas, key = 'unique')
            col_num_y = st.selectbox('Selecione o valor de y ', colunas_numericas, key = 'unique')
            col_color = st.selectbox('Selecione a coluna para cor', colunas)
            st.markdown('Selecione os valores de x e y')
            st.write(criar_scatterplot(col_num_x, col_num_y, col_color, df))

        if view == 'Correlação':
            if demo:
                st.markdown("Nota: nesta versão ainda não temos suporte para correlação com colunas categóricas")
            st.markdown('Gráfico de correlação das colunas númericas')
            st.write(cria_correlationplot(df, colunas_numericas))


if __name__ == '__main__':
    main()
