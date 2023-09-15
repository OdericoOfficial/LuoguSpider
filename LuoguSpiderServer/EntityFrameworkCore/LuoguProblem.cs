namespace LuoguSpiderServer.EntityFrameworkCore
{
#nullable disable
    public class LuoguProblem
    {
        public string Id { get; set; }

        public string Title { get; set; }
        
        public string Difficulty { get; set; }

        public string Keywords { get; set; }

        public string ProblemHtml { get; set; }

        public string SolutionHtml { get; set; }
    }
}
