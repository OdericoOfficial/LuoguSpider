using LuoguSpiderServer.EntityFrameworkCore;
using ModuleDistributor;
using ModuleDistributor.DependencyInjection;
using ModuleDistributor.EntityFrameworkCore;
using ModuleDistributor.Serilog;

namespace LuoguSpiderServer
{
    [DependsOn(typeof(SerilogModule),
        typeof(EntityFrameworkCoreModule<LuoguSpiderDbContext, SqliteOptionsWrapper>),
        typeof(InjectServiceModule))]
    public class LuoguSpiderServerModule : CustomModule
    {
        /// <summary>
        /// 通过Attribute反射，模块已经简单配置好了需要配置的内容
        /// 下面的方法只需要配置在Server项目下需要的内容就行了
        /// </summary>
        /// <param name="context">包含WebApplicationBuilder常用接口的上下文</param>
        public override void ConfigureServices(ServiceContext context)
        {
            context.Services.AddMasaBlazor();
            context.Services.AddRazorPages();
            context.Services.AddServerSideBlazor();
        }

        /// <summary>
        /// 通过Attribute反射，模块已经简单配置好了需要配置的内容
        /// 下面的方法只需要配置在Server项目下需要的内容就行了
        /// </summary>
        /// <param name="context">包含WebApplication常用接口的上下文</param>
        public override void OnApplicationInitialization(ApplicationContext context)
        {
            if (!context.Environment.IsDevelopment())
            {
                context.App.UseExceptionHandler("/Error");
                context.App.UseHsts();
            }

            context.App.UseHttpsRedirection();
            context.App.UseStaticFiles();
            context.App.UseRouting();
            context.EndPoint.MapBlazorHub();
            context.EndPoint.MapFallbackToPage("/_Host");
        }
    }
}
