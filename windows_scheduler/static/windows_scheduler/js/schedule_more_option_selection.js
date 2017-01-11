(function($) {
//  $("#id_schedule_choice_3").prop("checked", true);
   $(document).ready(function(){
     //ONCE
       $(':radio[id="id_schedule_choice_0"]').click(function(){
         if($(this).is(":checked")){
           $('.form-row.field-schedule_option_recur').hide();
           $('.form-row.field-schedule_option_week').hide();
           $('.form-row.field-schedule_option_month').hide();
           $('.form-row.field-schedule_option_month_option').hide();
           $('.form-row.field-schedule_option_month_day').hide();
           $('.form-row.field-schedule_option_month_on').hide();
           $('.form-row.field-schedule_option_month_on_day').hide();
           $('.form-row.field-schedule_end').hide();

         }
       });
     });
     $(document).ready(function(){
       //MINUTE
         $(':radio[id="id_schedule_choice_1"]').click(function(){
           if($(this).is(":checked")){
             $("#id_schedule_option_recur").attr("disabled", false);
             $('.form-row.field-schedule_option_recur').show();
             $('div.form-row.field-schedule_option_recur > div > p.help').text("Days (1 - 365)");
             $('.form-row.field-schedule_option_week').hide();
             $('.form-row.field-schedule_option_month').hide();
             $('.form-row.field-schedule_option_month_option').hide();
             $('.form-row.field-schedule_option_month_day').hide();
             $('.form-row.field-schedule_option_month_on').hide();
             $('.form-row.field-schedule_option_month_on_day').hide();
             $('.form-row.field-schedule_end').show();

           }
         });
       });
       $(document).ready(function(){
         //HOURLY
           $(':radio[id="id_schedule_choice_2"]').click(function(){
             if($(this).is(":checked")){
               $('.form-row.field-schedule_option_week').show();
               $('.form-row.field-schedule_option_recur').show();
               $('div.form-row.field-schedule_option_recur > div > p.help').text("Weeks (1 - 52)");
               $('.form-row.field-schedule_option_month').hide();
               $('.form-row.field-schedule_option_month_option').hide();
               $('.form-row.field-schedule_option_month_day').hide();
               $('.form-row.field-schedule_option_month_on').hide();
               $('.form-row.field-schedule_option_month_on_day').hide();
               $('.form-row.field-schedule_end').show();

             }
           });
         });
         $(document).ready(function(){
           //DAILY
             $(':radio[id="id_schedule_choice_3"]').click(function(){
               if($(this).is(":checked")){
                $('.form-row.field-schedule_option_month').show();
                $('.form-row.field-schedule_option_month_option').show();
                $('.form-row.field-schedule_option_month_day').show();
                 $('.form-row.field-schedule_option_recur').hide();
                 $('div.form-row.field-schedule_option_recur > div > p.help').text("Months (1 - 12)");
                 $('.form-row.field-schedule_option_week').hide();

                 $('.form-row.field-schedule_end').show();

               }
             });
           });

               $(document).ready(function(){
                 //MONTHLY
                   $(':radio[id="id_schedule_option_month_option_0"]').click(function(){
                     if($(this).is(":checked")){
                        $('.form-row.field-schedule_option_month_day').show();
                        $('.form-row.field-schedule_option_month_on').hide();
                        $('.form-row.field-schedule_option_month_on_day').hide();
                     }
                   });
                 });

               $(document).ready(function(){
                 //MONTHLY
                   $(':radio[id="id_schedule_option_month_option_1"]').click(function(){
                     if($(this).is(":checked")){
                        $('.form-row.field-schedule_option_month_day').hide();
                        $('.form-row.field-schedule_option_month_on').show();
                        $('.form-row.field-schedule_option_month_on_day').show();
                     }
                   });
                 });


               $(document).ready(function(){
                 //1 One Time 2 DAILY 3 WEEKLY 4 MONTHLY
                 var freq = $('input[name=schedule_choice]:checked').val();
                 if (freq == 1) {
                   $('.form-row.field-schedule_option_recur').hide();
                   $('.form-row.field-schedule_end').hide();
                    if ($('#id_schedule_option_repeat').is(":checked"))
                      {
                         $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').show();
                       }
                     else {
                         $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').hide();
                     }
                   }

                 else if(freq == 2){
                    $('div.form-row.field-schedule_option_recur > div > p.help').text("Days (1 - 365)");
                      if ($('#id_schedule_option_repeat').is(":checked"))
                        {
                           $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').show();
                         }
                       else {
                           $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').hide();
                       }
                     }


                  else if(freq == 3)
                     {
                       $('.form-row.field-schedule_option_week').show();
                       $('div.form-row.field-schedule_option_recur > div > p.help').text("Weeks (1 - 52)");
                         if ($('#id_schedule_option_repeat').is(":checked"))
                           {
                              $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').show();
                            }
                          else {
                              $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').hide();
                          }
                        }

                else if(freq == 4)
                    {
                      $('.form-row.field-schedule_option_month').show();
                       $('.form-row.field-schedule_option_month_option').show();
                      $('.form-row.field-schedule_option_recur').hide();
                      var mo = $('input[name=schedule_option_month_option]:checked').val();
                        if (mo == 1)
                        {
                        $('.form-row.field-schedule_option_month_day').show();
                        $('.form-row.field-schedule_option_month_on').hide();
                        $('.form-row.field-schedule_option_month_on_day').hide();
                        }
                        else {

                          $('.form-row.field-schedule_option_month_on').show();
                          $('.form-row.field-schedule_option_month_on_day').show();
                          $('.form-row.field-schedule_option_month_day').hide();
                        }
                        if ($('#id_schedule_option_repeat').is(":checked"))
                          {
                             $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').show();
                           }
                         else {
                             $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').hide();
                         }
                    }
                else {
                      //window.console&&console.log('Hello ' + freq);
                    }
                 });

                  $(document).ready(function(){
                    $(':checkbox[id="id_schedule_option_repeat"]').click(function(){
                      if($(this).is(":checked")){
                          $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').show();
                        }
                      else {
                          $('.form-row.field-schedule_option_task_interval.field-schedule_option_duration').hide();
                      }
                    });
                  });

     })(django.jQuery);
