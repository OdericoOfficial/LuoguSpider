using BlazorComponent;
using LuoguSpiderServer.EntityFrameworkCore;
using Masa.Blazor;
using Microsoft.AspNetCore.Components;
using Microsoft.EntityFrameworkCore;
using ModuleDistributor.Logging;

namespace LuoguSpiderServer.Pages
{
#nullable disable
    public partial class Explorer : ILoggerProxy
    {
        [Parameter]
        public string Id { get; set; }

        [Parameter]
        public string Type { get; set; }

        [Inject]
        public ILogger<Explorer> Logger { get; set; }
        ILogger ILoggerProxy.Logger { get => Logger; }

        [Inject]
        public LuoguSpiderDbContext Context { get; set; }

        private string _source;
        
        [ExLogging]
        protected override async Task OnInitializedAsync()
        {
            LuoguProblem problem = await Context.Set<LuoguProblem>().FirstOrDefaultAsync(item => item.Id == Id);
            if (problem is not null)
                _source = Type == "solutions" ? problem.SolutionHtml : problem.ProblemHtml;
            throw new ArgumentNullException("Problem cannot find.");
        }
    }
}
