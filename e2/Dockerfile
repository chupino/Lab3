from mcr.microsoft.com/dotnet/sdk:8.0
run dotnet new blazor -n BlazorApp
workdir BlazorApp
copy TodoItem.cs .
copy Todo.razor ./Components/Pages
copy NavMenu.razor ./Components/Layout
run dotnet build
cmd dotnet run --urls="http://0.0.0.0:80"
