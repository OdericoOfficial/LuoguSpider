using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using ModuleDistributor.Serilog;
using ModuleDistributor;

namespace LuoguSpiderServer
{
    public class Program
    {
        /// <summary>
        /// 自己按照ABP框架写的模块化小工具，利用静态织入工具实现aop配置简单的日志
        /// 后面的try catch块也使用aop的方式来重用
        /// </summary>
        /// <param name="args"></param>
        /// <returns></returns>
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