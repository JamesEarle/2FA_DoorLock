var cmd = require('node-cmd')
var gpio = require('gpio')

// function to take photo and return back promise
function capturePhoto () {
  console.log('>>> Capturing Photo <<<')
  var promise = new Promise(
    function (resolve, reject) {
      // Capture picture and save it as 'outut.jpg' in directory
      // Resolve in callback
      cmd.get('raspistill -o output.jpg -q 40', function () {
        return resolve('Photo Done')
      })
    }
  )
  return promise
}

//
var gpio4 = gpio.export(4, {
  direction: 'in',
  ready: function () {
  }
})

// bind to the "change" event
gpio4.on('change', function (val) {
   // value will report either 1 or 0 (number) when the value changes
  if (val === 1) {
    capturePhoto()
      .then((status) => {
        console.log('***************************')
        console.log(status)
        console.log('***************************')
      })
      .catch((error) => {
        console.log(error)
      })
  }
})

