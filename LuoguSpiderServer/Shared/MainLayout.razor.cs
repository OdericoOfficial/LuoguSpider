using LuoguSpiderServer.Pages;
using Masa.Blazor.Presets;
using Microsoft.AspNetCore.Components;
using Microsoft.JSInterop;
using ModuleDistributor.Logging;

namespace LuoguSpiderServer.Shared
{
#nullable disable
    public partial class MainLayout : ILoggerProxy<MainLayout>
    {
        private PPageTabs _pageTabs;

        [Inject]
        public NavigationManager Navigation { get; set; }

        [Inject]
        public ILogger<MainLayout> Logger { get; set; }
        ILogger ILoggerProxy.Logger { get => Logger; }

        private TabOptions TabOptions(PageTabPathValue pathValue)
        {
            var tokens = pathValue.AbsolutePath.Split('/');
            if (tokens.Length < 3)
                return new TabOptions("主页", "mdi-home-outline", "font-weight-bold");
            else
                if (tokens[1] == "solutions")
                    return new TabOptions($"{tokens[2]}题解", "mdi-book-check-outline", "font-weight-bold");
                else
                    return new TabOptions($"{tokens[2]}题目", "mdi-book-edit-outline", "font-weight-bold");
        }

        [Logging]
        private void NavigateTo()
            => Navigation!.NavigateTo("/");
    }
}
