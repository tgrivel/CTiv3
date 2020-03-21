    # Download javascript bibliotheken
    
    $bieb = (
    "https://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.2/jquery.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jqueryui-touch-punch/0.2.3/jquery.ui.touch-punch.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/PapaParse/4.1.2/papaparse.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/chosen/1.4.2/chosen.jquery.js",
    "https://cdn.plot.ly/plotly-basic-latest.min.js",
    "https://code.jquery.com/jquery-3.3.1.min.js")

    foreach ($boek in $bieb) {
        $out = $boek -split '/'
        Invoke-WebRequest $boek -UseBasicParsing -OutFile $out[-1]
    }