const express = require('express');
const bodyParser = require('body-parser');
const mongoClient = require('mongodb');

const app = express()

app.use(bodyParser.urlencoded({extended: true}))
app.use(express.static(__dirname + '/static'))
app.set('view engine', 'ejs')

var port = process.env.SERVER_PORT || 3000;

mongoClient.connect('mongodb://abhishek:abhishek@ds143000.mlab.com:43000/go-links', (err, database) => {
  if (err) return console.log(err)
  db = database
  app.listen(port, () => {
    console.log('listening on ' + port)
  })
})

app.get('/', (req, res) => {
  db.collection('links').find().toArray(function(err, results) {
    if (err) return console.log(err)
    res.render('index.ejs', {links: results})
  })
})

app.get('*', (req, res) => {
  db.collection('links').find().toArray(function(err, results) {
    if (err) return console.log(err)
    request_url = req.url.slice(1)
    redirect_path = '/'

    for (var i in results) {
      if (results[i].shortcut === request_url) {
        redirect_path = results[i].link
        break
      }
    }
    res.redirect(redirect_path)
  })
})

app.post('/links', (req, res) => {
  db.collection('links').save(req.body, (err, result) => {
    if (err) return console.log(err)

    console.log('saved to database')
    console.log(req.body)
    res.redirect('/')
  })
})

app.post('/delete', (req, res) => {
  db.collection('links').findOneAndDelete(
    {shortcut: req.body.shortcut}, (err, result) => {
      if(err) return res.send(500, err)
      console.log('removed from database.')
      res.redirect('/')
  })
})
