from mcr.microsoft.com/dotnet/SDK:8.0
run dotnet new blazor -n BlazorApp
workdir BlazorApp
copy *.razor ./Components/Pages
run dotnet build
cmd dotnet run --urls="http://0.0.0.0:80"