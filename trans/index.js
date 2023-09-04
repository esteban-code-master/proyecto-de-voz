const translate = require('translate-google')

translate('hola como estas', {to: 'es'}).then(res => {
    console.log(res)
}).catch(err => {
    console.error(err)
})