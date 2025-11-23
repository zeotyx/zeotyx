using System;
using System.Diagnostics;
using System.IO;

class FastSolver_Streaming
{
    static void Main()
    {
        Console.WriteLine("Press G to generate, F to read uploaded file, or type/paste an equation:");
        var key = Console.ReadKey(intercept: true);
        Console.WriteLine();

        var parser = new StreamingParser();
        string previewStart = "";
        string previewEnd = "";

        if (key.Key == ConsoleKey.G)
        {
            Console.WriteLine("How many terms per side?");
            if (!long.TryParse(Console.ReadLine(), out long t) || t < 1) t = 1000;

            Console.WriteLine("Choose output mode: 1=Preview, 2=Save Full Equation, 3=None");
            var mode = Console.ReadKey(intercept: true).KeyChar;
            Console.WriteLine();

            StreamWriter? file = null;
            if (mode == '2') file = new StreamWriter("/mnt/data/generated_equation.txt");

            var rnd = new Random();
            var sw = Stopwatch.StartNew();

            void genSide(long count)
            {
                for (long i = 0; i < count; i++)
                {
                    char s1 = rnd.Next(0, 2) == 0 ? '+' : '-';
                    int n1 = rnd.Next(1, 20);
                    char s2 = rnd.Next(0, 2) == 0 ? '+' : '-';
                    int n2 = rnd.Next(1, 20);

                    WriteTerm(s1, n1, true);
                    WriteTerm(s2, n2, false);
                }
            }

            void WriteTerm(char sign, int num, bool x)
            {
                if (mode == '1')
                {
                    if (previewStart.Length < 1000) previewStart += sign + num.ToString() + (x ? "x" : "");
                    else previewEnd += sign + num.ToString() + (x ? "x" : "");
                }
                if (mode == '2') file!.Write(sign.ToString() + num.ToString() + (x ? "x" : ""));
                parser.Feed(sign);
                foreach (var ch in num.ToString()) parser.Feed(ch);
                if (x) parser.Feed('x');
            }

            genSide(t);
            parser.FlipSide();
            if (mode == '2') file!.Write("=");
            genSide(t);

            parser.Finish();
            sw.Stop();
            file?.Close();
            Output(parser, sw.ElapsedMilliseconds, mode, previewStart, previewEnd);
            return;
        }

        if (key.Key == ConsoleKey.F)
        {
            string uploadedPath = "/mnt/data/do you want to type your own equati.txt";
            if (!File.Exists(uploadedPath))
            {
                Console.WriteLine("Uploaded file not found.");
                return;
            }

            Console.WriteLine("Mode: 1=Preview  2=None");
            var mode = Console.ReadKey(intercept: true).KeyChar;
            Console.WriteLine();

            var sw = Stopwatch.StartNew();
            using var sr = new StreamReader(uploadedPath);
            char[] buf = new char[65536];
            int r;
            bool onRight = false;

            while ((r = sr.Read(buf, 0, buf.Length)) > 0)
            {
                for (int i = 0; i < r; i++)
                {
                    char ch = buf[i];
                    if (mode == '1')
                    {
                        if (previewStart.Length < 200) previewStart += ch;
                        else previewEnd += ch;
                    }
                    parser.Feed(ch);
                }
            }

            parser.Finish();
            sw.Stop();
            Output(parser, sw.ElapsedMilliseconds, mode, previewStart, previewEnd);
            return;
        }

        string input = Console.ReadLine() ?? "";
        Console.WriteLine("Mode: 1=Preview  2=None");
        var pm = Console.ReadKey(intercept: true).KeyChar;
        Console.WriteLine();

        var sw2 = Stopwatch.StartNew();
        foreach (var ch in input)
        {
            if (pm == '1')
            {
                if (previewStart.Length < 200) previewStart += ch;
                else previewEnd += ch;
            }
            parser.Feed(ch);
        }
        parser.Finish();
        sw2.Stop();

        Output(parser, sw2.ElapsedMilliseconds, pm, previewStart, previewEnd);
    }

    static void Output(StreamingParser p, long ms, char mode, string start, string end)
    {
        Console.WriteLine();
        if (mode == '1')
        {
            Console.WriteLine("Preview:");
            Console.WriteLine(start);
            Console.WriteLine("... (middle skipped) ...");
            Console.WriteLine(end);
            Console.WriteLine();
        }
        if (mode == '2') Console.WriteLine("Full equation saved to file.");

        long totalX = p.LeftX - p.RightX;
        long totalC = p.RightC - p.LeftC;

        if (totalX == 0)
        {
            if (totalC == 0) Console.WriteLine("Infinite solutions.");
            else Console.WriteLine("No solution.");
        }
        else
        {
            Console.WriteLine($"{totalX}x = {totalC}");
            Console.WriteLine($"x = {(double)totalC / totalX}");
        }
        Console.WriteLine($"Time: {ms} ms");
    }
}

class StreamingParser
{
    public long LeftX { get; private set; }
    public long LeftC { get; private set; }
    public long RightX { get; private set; }
    public long RightC { get; private set; }

    bool onRight;
    int sign = 1;
    long num = 0;
    bool hasDigits;

    public void Feed(char ch)
    {
        if (ch == '+') { Flush(); sign = 1; return; }
        if (ch == '-') { Flush(); sign = -1; return; }
        if (ch == '=') { Flush(); onRight = true; sign = 1; return; }
        if ((uint)(ch - '0') <= 9) { hasDigits = true; num = num * 10 + (ch - '0'); return; }
        if (ch == 'x')
        {
            long v = hasDigits ? num : 1;
            if (!onRight) LeftX += sign * v; else RightX += sign * v;
            num = 0;
            hasDigits = false;
            return;
        }
    }

    void Flush()
    {
        if (hasDigits)
        {
            if (!onRight) LeftC += sign * num; else RightC += sign * num;
            num = 0;
            hasDigits = false;
        }
    }
    public void FlipSide()
    {
        Flush();
        onRight = true;
        sign = 1;
        num = 0;
        hasDigits = false;
    }

    public void Finish() => Flush();
}
