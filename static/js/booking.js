function handler(id){
    const date = $(`#date${id}`).val()
    const msg = `the message is #channel${id}`
    // const channel_id = $(`#channel${id} :selected`).val();
    const channel_id = $(`#channel${id}`).val();
    // $('#drzava').find(":selected").val(); 

    $(`#slot${id}`).empty();


    const payload = {
        "date" : date,
        "channel_id" : channel_id
    }

    fetch(`${window.origin}/api/getbookings`, {
        method: "POST",
        body: JSON.stringify(payload),
        headers: new Headers({
          "content-type": "application/json"
        })
      })
      .then(function(response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(function(data) {
          
          data.all_slots.forEach(function (item, index) {
            $(`#slot${id}`).append(`<option value=${item['slot_id']}>${item['desc']}</option>`)
          });

        $(`#slot${id} > option`).each(function(){
          if (data.slots_taken.includes(parseInt(this.value)) ){
            console.log(this);
            $(this).attr('disabled',true)
          }
        })



        //     // Function to enable all disbaled radios
        //     var x = document.getElementsByClassName("radio");
        //     var i;
        //     for (i = 0; i < x.length; i++) {
        //         x[i].disabled = false;
        //         x[i].checked = false;
        //     } 

        //     // Function to disable all inputs before start date

        //     // get start date
        //     const startdate = new Date($("#c_start_date").val())
        //     // get input date
        //     const date = new Date($("#date").val())

        //     // if input date before start date
        //     if(startdate > date){
        //         var x = document.getElementsByClassName("radio");
        //         var i;
        //         for (i = 0; i < x.length; i++) {
        //             x[i].disabled = true;
        //             x[i].checked = false;
        //         } 
        //     }
        
            
        //     // Disable radios that are already taken
        //     var slotArray = data.slots_taken;
        //     var arrayLength = slotArray.length;
        //     for (var i = 0; i < arrayLength; i++) {
        //         document.getElementById(`checkbox${slotArray[i]}`).disabled = true;
        //     }
        // 
      });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });

  }
  