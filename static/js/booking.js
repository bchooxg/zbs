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

      });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });

  }
  