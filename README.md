# rasterLab

## Laboratório para aulas de Processamento Digital de Imagens

# link deste repositório: https://github.com/mmamorim/rasterLab

### Como usar? veja (index.html / main.js) 

```javascript
import imageLab from "./imageLab/imageLab.js"

console.log('imageLab', imageLab);
imageLab.setLoadButtonID('btnLoad')
```

### Como criar um filtro? (main.js) 

criar um novo arquivo exportando uma função e adicionar na lista de filtros...veja exemplo no arquivo filtros/brilho.js

```javascript
function brilho(imageLab) {

}
export default brilho
```

```javascript
createFilters(imageLab, [
    { label: 'Brilho', method: brilho },
    ...
])
```

### Trecho padrão para percorrer todos os pixels 

```javascript
for(let y=1; y <= imageLab.image1.height; y++) {
    for(let x=1; x <= imageLab.image1.width; x++) {
        let pixel = imageLab.image1.getPixel(x,y)
        // processamento de cada pixel da imagem
    }
}
imageLab.image2.refresh()
```

[Sobre a foto da Lena](https://en.wikipedia.org/wiki/Lenna)

[Sepia algorithm](https://leware.net/photo/blogSepia.html) 