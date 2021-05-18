from tech_news import scrape_noticia
from tech_news import fetch

scrape_noticia(
    fetch(
        "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities"
        + "/155000-musk-tesla-carros-totalmente-autonomos.htm"
    )
)
