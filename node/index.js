var fetch = require('node-fetch')
var fs = require('fs')
var gpio = require('gpio')
var cmd = require('node-cmd')

// Setup button GPIO pin 23
var button = gpio.export(4, {
  direction: 'in',
  ready: function () {
  }
})

// Setup Green Face GPIO pin 18
var gpio18 = gpio.export(18, {
  direction: 'out',
  ready: function () {
    gpio18.set()
    setTimeout(function () { gpio18.reset() }, 1000)
  }
})

// Setup Red Face GPIO pin 22
var gpio22 = gpio.export(22, {
  direction: 'out',
  ready: function () {
    gpio22.set()
    setTimeout(function () { gpio22.reset() }, 1000)
  }
})

// Setup Green Voice GPIO pin 17
var gpio17 = gpio.export(17, {
  direction: 'out',
  ready: function () {
    gpio17.set()
    setTimeout(function () { gpio17.reset() }, 1000)
  }
})

// Setup Red Voice GPIO 27
var gpio27 = gpio.export(27, {
  direction: 'out',
  ready: function () {
    gpio27.set()
    setTimeout(function () { gpio27.reset() }, 1000)
  }
})

function capturePhoto () {
  console.log('>>> Capturing Photo <<<')
  var promise = new Promise(
    function (resolve, reject) {
      // Capture picture and save it as 'outut.jpg' in directory
      cmd.get('raspistill -o output.jpg -q 40', function () {
        return resolve('Photo Done')
      })
    }
  )
  return promise
}

function captureAudio (status) {
  console.log('***************************')
  console.log(status)
  console.log('***************************')
  console.log('>>> Capturing Audio <<<')
  var promise = new Promise(
    function (resolve, reject) {
      // Capture audio and save it as 'voice_recording.wav' in directory
      cmd.get('arecord -D plughw:1 -d 5 -f S16 -r 16000 voice_record.wav', function () {
        return resolve('Audio Done')
      })
    }
  )
  return promise
}

function detectPhoto (status) {
  console.log(status)
  var promise = new Promise(
    function (resolve, reject) {
      fs.readFile('./output.jpg', function (err, data) {
        if (err) reject('Failed! Unable to read photo') // Fail if the file can't be read.

        return fetch('https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '<Cognitive Service Face Key>'
          },
          body: data
        }).then(response => {
          return response.json()
        }).then(json => {
        // Read response JSON here...
        // Verification success.. light green
          console.log(json)
          var faceId = json[0]['faceId']
          console.log('***************************')
          console.log('Photo Detected: Success')
          console.log('***************************')
          return resolve(faceId)
        }).catch(err => {
          // Verification failed.. light red
          console.log('***************************')
          console.log('Photo Detected: Failed')
          console.log('***************************')
          console.log(err)
          gpio22.set()
          return reject('Photo Detected: Failed')
        })
      })
    }
  )
  return promise
}

function verifyPhoto (faceId) {
  console.log('faceId:', faceId)
  var promise = new Promise(
    function (resolve, reject) {
      return fetch('https://westus.api.cognitive.microsoft.com/face/v1.0/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Ocp-Apim-Subscription-Key': '<Cognitive Service Face Key>'
        },
        body: JSON.stringify({
          'faceId1': '<faceId to compare (run face detect API to get faceId)>',
          'faceId2': faceId
        })
      }).then(response => {
        return response.json()
      }).then(json => {
        // Read response JSON here...
        // Verification success.. light green
        console.log(json)
        var isIdentical = json['isIdentical']
        if (isIdentical) {
          gpio18.set()
          return resolve('Photo Verification: Passed')
        } else {
          gpio22.set()
          return reject('Photo Verify: Failed')
        }
      }).catch(err => {
        // Verification failed.. light red
        console.log('***************************')
        console.log('Photo Verify: Failed')
        console.log('***************************')
        console.log(err)
        gpio22.set()
        return reject('Photo Verify: Failed')
      })
    }
  )
  return promise
}

function verifyAudio (status) {
  console.log(status)
  var promise = new Promise(
    function (resolve, reject) {
      fs.readFile('./voice_record.wav', function (err, data) {
        if (err) reject('Failed! Unable to read audio') // Fail if the file can't be read.

        return fetch('https://westus.api.cognitive.microsoft.com/spid/v1.0/verify?verificationProfileId=49fffc7a-5ea0-4da7-b615-a26deb3a11b7', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '<Cognitive Service Voice Key>'
          },
          body: data
        }).then(response => {
          return response.json()
        }).then(json => {
        // Read response JSON here...
        // Verification success.. light green
          console.log(json)
          var isAccepted = json['result']
          if (isAccepted === 'Accept') {
            gpio17.set()
            return resolve('Audio Verification: Passed')
          } else {
            gpio27.set()
            return reject('Audio Verify: Failed')
          }
        }).catch(err => {
        // Verification failed.. light red
          console.log('***************************')
          console.log('Audio Verify: Failed')
          console.log('***************************')
          console.log(err)
          gpio27.set()
          return reject('Audio Verify: Failed')
        })
      })
    }
  )
  return promise
}

// bind to the "change" event
button.on('change', function (val) {
  // value will report either 1 or 0 (number) when the value changes
  if (val === 1) {
    capturePhoto()
      .then(detectPhoto)
      .then(verifyPhoto)
      .then(captureAudio)
      .then(verifyAudio)
      .then((status) => {
        console.log('***************************')
        console.log(status)
        console.log('***************************')
      })
      .catch((error) => {
        console.log('***************************')
        console.log(error)
        console.log('***************************')
      })
  }
})
