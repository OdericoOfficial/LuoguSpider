using LuoguSpiderServer.EntityFrameworkCore;
using ModuleDistributor;
using ModuleDistributor.EntityFrameworkCore;
using ModuleDistributor.Serilog;

namespace LuoguSpiderServer
{
    [DependsOn(typeof(SerilogModule),
        typeof(EntityFrameworkCoreModule<LuoguSpiderDbContext, SqliteOptionsWrapper>))]
    public class LuoguSpiderServerModule : CustomModule
    {
        public override void ConfigureServices(ServiceContext context)
        {
            context.Services.AddRazorPages();
            context.Services.AddServerSideBlazor();
        }

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
