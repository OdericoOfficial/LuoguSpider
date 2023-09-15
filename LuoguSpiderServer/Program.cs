using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using ModuleDistributor.Serilog;
using ModuleDistributor;

namespace LuoguSpiderServer
{
    public class Program
    {
        /// <summary>
        /// �Լ�����ABP���д��ģ�黯С���ߣ����þ�̬֯�빤��ʵ��aop���ü򵥵���־
        /// �����try catch��Ҳʹ��aop�ķ�ʽ������
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