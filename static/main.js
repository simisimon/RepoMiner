function ClearAll()
{
    console.log("clear all")

    Clear();

    var table = document.getElementById("table");
    if(typeof(table) != 'undefined' && table != null)
    {
        table.parentNode.removeChild(table);
    }

    var map = document.getElementById("treemap");
    if(typeof(map) != 'undefined' && map != null)
    {
        map.parentNode.removeChild(map);
    }

    var name = document.getElementById("projectName");
    if(typeof(name) != 'undefined' && name != null)
    {
        name.parentNode.removeChild(name);
    }

    var commits = document.getElementById("commits");
    if(typeof(commits) != 'undefined' && commits != null)
    {
        commits.parentNode.removeChild(commits);
    }

    var files = document.getElementById("files");
    if(typeof(files) != 'undefined' && files != null)
    {
        files.parentNode.removeChild(files);
    }

    var methods = document.getElementById("methods");
    if(typeof(methods) != 'undefined' && methods != null)
    {
        methods.parentNode.removeChild(methods);
    }
}

function Clear()
{
    console.log("clear");

    document.getElementById("input").value = '';
    document.getElementById("commit1").value = '';
    document.getElementById("commit2").value = '';
    document.getElementById("date1").value = '';
    document.getElementById("date2").value = '';
}

function SwitchTables()
{
    console.log("Switch tables");

    var select = document.getElementById("table-select");
    if(select.options[select.selectedIndex].value == "all")
    {
        document.getElementById("all_methods_wrapper").style.display = "block"
        document.getElementById("only_methods_wrapper").style.display = "none"
        document.getElementById("test_methods_wrapper").style.display = "none"
    }
    else if(select.options[select.selectedIndex].value == "only")
    {
        document.getElementById("all_methods_wrapper").style.display = "none"
        document.getElementById("only_methods_wrapper").style.display = "block"
        document.getElementById("test_methods_wrapper").style.display = "none"
    }
    else if(select.options[select.selectedIndex].value == "test")
    {
        document.getElementById("all_methods_wrapper").style.display = "none"
        document.getElementById("only_methods_wrapper").style.display = "none"
        document.getElementById("test_methods_wrapper").style.display = "block"
    }

}

function UpdateCommitFields() 
{
    console.log('update');

    var select = document.getElementById("select");
    if(select.options[select.selectedIndex].value == 'single')
    {
        document.getElementById("commit1").style.display = "block";
        document.getElementById("commit1").disabled=false;
        document.getElementById("commit2").style.display = "none";
        document.getElementById("commit2").disabled=true;
        document.getElementById("date1").style.display = "none";
        document.getElementById("date1").disabled=true;
        document.getElementById("date2").style.display = "none";
        document.getElementById("date2").disabled=true;
    }
    else if(select.options[select.selectedIndex].value == 'fromTo')
    {
        document.getElementById("commit1").style.display = "block";
        document.getElementById("commit1").disabled=false;
        document.getElementById("commit2").style.display = "block";
        document.getElementById("commit2").disabled=false;
        document.getElementById("date1").style.display = "none";
        document.getElementById("date1").disabled=true;
        document.getElementById("date2").style.display = "none";
        document.getElementById("date2").disabled=true;
    }
    else if(select.options[select.selectedIndex].value == 'sinceTo')
    {
        document.getElementById("date1").style.display = "block";
        document.getElementById("date1").disabled=false;
        document.getElementById("date2").style.display = "block";
        document.getElementById("date2").disabled=false;
        document.getElementById("commit1").style.display = "none";
        document.getElementById("commit1").disabled=true;
        document.getElementById("commit2").style.display = "none";
        document.getElementById("commit2").disabled=true;
    }
}


function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("results");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function activeSubmitButton(obj)
{
    if(obj.value.length >= 1)
    {
        document.getElementById("start").disabled=false;
    }
    else
    {
        document.getElementById("start").disabled=true;
    }
}

