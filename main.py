import scrapy

class PokeSpider(scrapy.Spider):
    name = 'pokemons'
    start_urls = ['https://pokemondb.net/pokedex/all']

    def parse(self, response):
        
        # Encontrando todas as linhas da tabela de Pokemons
        linhas = response.css('table.data-table tbody tr')

        for linha in linhas:

            #Navegando na pagina principal  
            url = linha.css('td:nth-child(2) a::attr(href)').get()
          
            #Extraindo o nome do Pokémon
            nome = linha.css('td:nth-child(2) a::text').get()

            #Salvando informações extraidas
            yield response.follow(url, self.parse_pokemon, meta={'url': url, 'nome': nome})

    def parse_pokemon(self, response):

            #Buscando dados principais dos pokemons e concatenando com informações obtidas no for anterior
            id = response.css('table.vitals-table tr:nth-child(1) strong::text').get()
            url = response.meta['url']
            nome = response.meta['nome']
            altura = response.css('table.vitals-table tr:nth-child(4) td::text').get()
            peso = response.css('table.vitals-table tr:nth-child(5) td::text').get()
            tipos = response.css('table.vitals-table tr:nth-child(2) a::text').getall()

            #Encontrando as próximas evoluções
            evolucoes = []
            evolucoes_sel = response.css('div.infocard')
            for evolucao in evolucoes_sel:
                poke_num = evolucao.css('span a::text').get()
                nome = evolucao.css('span a::text').get()
                url = evolucao.css('span a::attr(href)').get()
                evolucoes.append({'PokéNum': poke_num, 'nome': nome, 'URL': url})

            #Encontrando as habilidades
            habilidades = []
            habilidades_sel = response.css('table.vitals-table tr:nth-child(6)')
            for habilidade in habilidades_sel:
                url = habilidade.css('span a::attr(href)').get()
                nome = habilidade.css('span a::text').get()
                descricao = habilidade.css('div.grid-row p a::text').get()
                habilidades.append({'URL': url, 'Nome': nome, 'Descrição': descricao})

            #Salvando os dados obtidos em variaveis
            pokemon_info = {
                        'Numero': id,
                        'URL da página': url,
                        'Nome': nome,
                        'Tamanho': altura,
                        'Peso': peso,
                        'Tipos': tipos,
                        'Próximas evoluções': evolucoes,
                        'Habilidades': habilidades,
                    }
      
            yield pokemon_info