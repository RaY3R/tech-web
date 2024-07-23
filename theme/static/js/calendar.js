const isExtraDays = (week, date) => {
  if (week === 0 && date > 10) {
    return true;
  } else if (week === 5 && date < 10) {
    return true;
  } else if (week === 4 && date < 10) {
    return true;
  } else {
    return false;
  }
};

if (new URLSearchParams(window.location.search).get("checkin")) {
  $("#checkin_date").text(
    new URLSearchParams(window.location.search).get("checkin")
  );
}

if (new URLSearchParams(window.location.search).get("checkout")) {
  $("#checkout_date").text(
    new URLSearchParams(window.location.search).get("checkout")
  );
}

if (new URLSearchParams(window.location.search).get("guests")) {
  $("#search_people_number").text(
    new URLSearchParams(window.location.search).get("guests")
  );
}

if (new URLSearchParams(window.location.search).get("location")) {
  $("#destination__input").val(
    new URLSearchParams(window.location.search).get("location")
  );
}

const render = (months, currentIndex) => {
  $("#left__calendar .month_title").text(months[currentIndex].name);
  $("#left__calendar .calendar__table").html(
    months[currentIndex].calendar.map((week, i) => {
      return `<tr class="calendar_days">${week
        .map((day) =>
          isExtraDays(i, day.number)
            ? `<td disabled="disabled"></td>`
            : `<td date="${day.date}" date-week="${day.week}"><span>${day.number}</span></td>`
        )
        .join("")}</tr>`;
    })
  );
  $("#right__calendar .month_title").text(months[currentIndex + 1].name);
  $("#right__calendar .calendar__table").html(
    months[currentIndex + 1].calendar.map((week, i) => {
      return `<tr class="calendar_days">${week
        .map((day) =>
          isExtraDays(i, day.number)
            ? `<td disabled="disabled"></td>`
            : `<td date="${day.date}" date-week="${day.week}"><span>${day.number}</span></td>`
        )
        .join("")}</tr>`;
    })
  );
  $(".calendar_days td").click((e) => {
    if (!e.target.classList.contains("selected")) {
      if (selectedCheckInDate == null) {
        e.target.classList.add("selected");

        selectedCheckInDate = e.target.parentElement.getAttribute("date");
        $("#checkin_date").text(
          moment(selectedCheckInDate).subtract(1, "day").format("YYYY-MM-DD")
        );
      } else if (selectedCheckOutDate == null) {
        selectedCheckOutDate = e.target.parentElement.getAttribute("date");
        e.target.classList.add("selected");
        $("#checkout_date").text(
          moment(selectedCheckOutDate).subtract(1, "day").format("YYYY-MM-DD")
        );
      }
      if (selectedCheckInDate && selectedCheckOutDate) {
        start = moment(selectedCheckInDate);
        end = moment(selectedCheckOutDate);
        $(`td[date="${start.toISOString()}"] span`)
          .parent()
          .addClass("selected-gray");
        while (start.isBefore(end)) {
          start.add(1, "day");
          months.forEach((month) => {
            month.calendar.forEach((week) => {
              week.forEach((day) => {
                if (day.date == start.toISOString()) {
                  $(`td[date="${day.date}"] span`)
                    .parent()
                    .addClass("selected-gray");
                }
              });
            });
          });
        }
      }
    } else {
      e.target.classList.remove("selected");
      if (selectedCheckInDate == e.target.parentElement.getAttribute("date")) {
        reset(true, true);
      }
      if (selectedCheckOutDate == e.target.parentElement.getAttribute("date")) {
        reset(false, true);
      }
    }
  });
};

moment.locale("it");
var current = moment();
var selectedCheckInDate = null;
var selectedCheckOutDate = null;
var months = [];

for (var i = 0; i < 12; i++) {
  if (i < current.month()) {
    continue;
  }
  months[i] = {};
  months[i].name = moment().month(i).format("MMMM") + " " + moment().year();
  months[i].days = moment().month(i).daysInMonth();
  months[i].calendar = [];
  const startDate = moment([months[i].name.split(" ")[1], i])
    .clone()
    .startOf("month")
    .startOf("week");

  const endDate = moment([months[i].name.split(" ")[1], i])
    .clone()
    .endOf("month");

  const day = startDate.clone().subtract(1, "day");

  // looping a month by a week
  while (day.isBefore(endDate, "day")) {
    months[i].calendar.push(
      Array(7)
        .fill(0)
        .map(() => {
          return {
            number: day.add(1, "day").clone().format("DD"),
            date: day.clone().add(1, "day").toISOString(),
            week: Math.ceil(day.clone().date() / 7),
            selected: false,
          };
        })
    );
  }
}

var currentIndex = current.month();

render(months, currentIndex);

$("#search__end_date").click(() => {
  if (!$("#people__popup").hasClass("hidden")) {
    $("#people__popup").toggleClass("hidden");
  }
  $("#calendar__popup").toggleClass("hidden");
});

$("#search__start_date").click(() => {
  if (!$("#people__popup").hasClass("hidden")) {
    $("#people__popup").toggleClass("hidden");
  }
  $("#calendar__popup").toggleClass("hidden");
});

$("#search__people").click(() => {
  if (!$("#calendar__popup").hasClass("hidden")) {
    $("#calendar__popup").toggleClass("hidden");
  }
  $("#people__popup").toggleClass("hidden");
});

$("#calendar__prev").click(() => {
  if (currentIndex > 0) {
    currentIndex -= 1;
    render(months, currentIndex);
  }
});
$("#calendar__next").click(() => {
  if (currentIndex < 10) {
    currentIndex += 1;
    render(months, currentIndex);
  }
});

const reset = (checkin, checkout) => {
  if (checkin) {
    selectedCheckInDate = null;
    $("#checkin_date").text("Seleziona una data");
    $(".selected").removeClass("selected");
  }
  if (checkout) {
    selectedCheckOutDate = null;
    $("#checkout_date").text("Seleziona una data");
  }
  $(".selected-gray").removeClass("selected-gray");
};

$("body").click((e) => {
  if (
    !$(e.target).closest("#calendar__popup").length &&
    !$(e.target).closest("#search__start_date").length &&
    !$(e.target).closest("#search__end_date").length &&
    !$(e.target).closest("#people__popup").length &&
    !$(e.target).closest("#search__people").length &&
    !$(e.target).closest("#autocomplete_location__popup").length &&
    !$(e.target).closest("#search__place").length
  ) {
    $("#calendar__popup").addClass("hidden");
    $("#people__popup").addClass("hidden");
    $("#autocomplete_location__popup").addClass("hidden");
  }
});

/* People Popup */

$("#remove_people").click(() => {
  let people = parseInt($("#people_number").text());
  if (people > 1) {
    $("#people_number, #search_people_number").text(people - 1);
    $("#people_number").attr("field-value", people - 1);
  }
});

$("#add_people").click(() => {
  let people = parseInt($("#people_number").text());
  $("#people_number, #search_people_number").text(people + 1);
  $("#people_number").attr("field-value", people + 1);
});

const triggerAutocomplete = () => {
  $.ajax("/api/location/autocomplete?q=" + $("#destination__input").val(), {
    method: "GET",
    success: function (data) {
      $("#autocomplete_location__popup").removeClass("hidden");
      $("#autocomplete_results").html("");
      data.forEach((item) =>
        $("#autocomplete_results").append(
          `<span class="autocomplete_item p-4 hover:bg-slate-200 rounded-xl cursor-pointer">${item}</span>`
        )
      );
    },
  });
};

$(document).on("click", ".autocomplete_item", (e) => {
  $("#autocomplete_location__popup").addClass("hidden");
  $("#destination__input").val(e.currentTarget.innerHTML);
});

$("#destination__input").on("input", triggerAutocomplete);
$("#destination__input").on("click", triggerAutocomplete);

$("#search__submit").on("click", () => {
  document.location = `/results?location=${$(
    "#destination__input"
  ).val()}&checkin=${$("#checkin_date").text()}&checkout=${$(
    "#checkout_date"
  ).text()}&guests=${$("#search_people_number").text()}`;
});
