using BlazorComponent;
using LuoguSpiderServer.EntityFrameworkCore;
using Masa.Blazor;
using Masa.Blazor.Presets;
using Microsoft.AspNetCore.Components;
using Microsoft.EntityFrameworkCore;
using System;
using System.ComponentModel.DataAnnotations;

namespace LuoguSpiderServer.Pages
{
    public partial class Index
    {
        class Model
        {
            public string Difficulty { get; set; } = "";
            public string Keywords { get; set; } = "";
            public string Serach { get; set; } = "";
        }

        private string _value = $"题目难度: , 标签: , 关键词: ";
        private Model _model = new();
        private List<DataTableHeader<LuoguProblem>> _headers = new List<DataTableHeader<LuoguProblem>>
        {
            new (){ Text= "题号", Value= nameof(LuoguProblem.Id), Sortable= false,},
            new (){ Text= "题目名称", Value= nameof(LuoguProblem.Title), Sortable= false,},
            new (){ Text= "标签", Value= nameof(LuoguProblem.Keywords), Sortable = false},
            new (){ Text= "难度", Value= nameof(LuoguProblem.Difficulty), Sortable = false},
            new (){ Text= "Actions", Value= "Actions", Sortable=false, Width="100px", Align=DataTableHeaderAlign.Center, }
        };
        private List<LuoguProblem> _list = new List<LuoguProblem>()
        {
            new LuoguProblem(),
            new LuoguProblem(),
            new LuoguProblem(),
            new LuoguProblem(),
            new LuoguProblem(),
        };
        private List<string> _items = new()
        {
            "",
            "入门",
            "普及−",
            "普及 提高−",
            "普及+ 提高",
            "提高+ 省选"
        };

        [Inject]
        public NavigationManager? Navigation { get; set; }

        [Inject]
        public LuoguSpiderDbContext? Context { get; set; }

        private async Task OnSubmitClick()
        {
            _value = $"题目难度: {_model.Difficulty}, 标签: {_model.Keywords}, 关键词: {_model.Serach}";
            _list = await Context!.Set<LuoguProblem>().Where(item => item.Difficulty.Contains(_model.Difficulty)
                            && item.Keywords.Contains(_model.Keywords)
                            && (item.Title.Contains(_model.Serach)
                            || item.Difficulty.Contains(_model.Serach)
                            || item.Keywords.Contains(_model.Serach))).OrderBy(item => item.Id).ToListAsync();
        }
        
        protected override async Task OnInitializedAsync()
        {
            if (Context is not null)
                _list = await (from item in Context.Set<LuoguProblem>()
                       orderby item.Id
                       select item).ToListAsync();
        }
    }
}