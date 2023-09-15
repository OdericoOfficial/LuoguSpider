using Masa.Blazor.Presets;
using Microsoft.AspNetCore.Components;
using Microsoft.JSInterop;

namespace LuoguSpiderServer.Shared
{
    public partial class MainLayout
    {
        private PPageTabs? _pageTabs;

        [Inject]
        public NavigationManager? Navigation { get; set; }  

        private TabOptions? TabOptions(PageTabPathValue pathValue)
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

        private void NavigateTo()
            => Navigation!.NavigateTo("/");
    }
}
