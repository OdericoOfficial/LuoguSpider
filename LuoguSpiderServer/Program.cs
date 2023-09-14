using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using ModuleDistributor.Serilog;
using ModuleDistributor;

namespace LuoguSpiderServer
{
    public class Program
    {
        [Serilog]
        public static async Task<int> Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            await builder.ConfigureServiceAsync<LuoguSpiderServerModule>();
            var app = builder.Build();
            await app.OnApplicationInitializationAsync();
            await app.RunAsync();
            return 0;
        }
    }
}