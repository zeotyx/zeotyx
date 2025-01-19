using System;
using System.ComponentModel.Design;
using System.Linq;
using System.Reflection;

namespace calculator_terminal
{
    internal class Program
    {
        static string[] calc = { "+", "-", "/", "*" };
        static void Main(string[] args)
        {
           




            while (true)
            {
                bool normalcal = false;
                MainScreen();
                string vysledek = "";
                string input = Console.ReadLine();
                input = input.ToLower();
                if (input == "show options")
                {
                    Console.Clear();
                    Console.WriteLine(@"THERE U CAN SEE CALCULATIONS U CAN DO
power2(x) = √x
sqrt(x) = x²");
                    Console.ReadKey();
                }
                else if (input.Contains("power2"))
                {
                    vysledek = Power(Getnum(input));
                }
                else if (input.Contains("sqr"))
                {
                    vysledek = Sqrt(Getnum(input));
                }
                else if (input.Contains(calc[0]) || input.Contains(calc[1]) || input.Contains(calc[2]) || input.Contains(calc[3]))
                {
                    normalcal = true;
                    Console.Clear();
                    vysledek = Calculation(input);
                }
                if (vysledek.Length > 1)
                {

                    Console.WriteLine(input + " = " + vysledek + "\nPress any button to continue");
                    Console.ReadKey();

                }
                else
                {
                    if (input!= "show options" || vysledek.Length < 1)
                    {
                        
                        Console.WriteLine(input + " = " + input + "\nPress any button to continue");
                        Console.ReadKey();
                    }
                    
                }
            }
            




        }



        static string  Calculation(string input)
        {
            bool firstD = true;
            string cislo1= "";
            string cislo2= "";
            string operators = "";
            double vysledek = 0;
            foreach (char c in input)
            {
                if (char.IsDigit(c))
                {
                    if (firstD == true)
                    {
                        cislo1 += c;
                    }
                    else
                    {
                        cislo2 += c;
                    }
                }
                else
                {
                    if (c == '+' || c == '-'|| c== '/' || c == '*')
                    {
                        firstD = false;
                        if (c == '+')
                        {
                            operators = c.ToString();
                        }
                        else if (c == '-')
                        {
                            operators = c.ToString();
                        }
                        else if (c == '/')
                        {
                            operators = c.ToString();
                        }
                        else if (c == '*')
                        {
                            operators = c.ToString();
                        }
                    }
                    
                }

            }

            if (operators == "+")
            {
                vysledek = Convert.ToDouble(cislo1) + Convert.ToDouble(cislo2);
            }
            else if (operators == "-")
            {
                vysledek = Convert.ToDouble(cislo1) - Convert.ToDouble(cislo2);
            }
            else if (operators == "/")
            {
                vysledek = Convert.ToDouble(cislo1) / Convert.ToDouble(cislo2);
            }
            else if (operators == "*")
            {
                vysledek = Convert.ToDouble(cislo1) * Convert.ToDouble(cislo2);
            }
            return vysledek.ToString();
        }

        static void MainScreen()
        {
            Console.Clear();
            Console.WriteLine(@"CALCULATOR


U can input ur calculation down there and it will calculate it or u can type (show options) for avaiable calc


↓↓↓               there u put ur calculations                  ↓↓↓

");

        }


        static string Getnum(string input)
        {
            bool getSQ = false;
            string cislo = "";
            
            char[] chars = input.ToLower().ToCharArray();
            string[] numbers = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" };
            foreach (char c in chars)
            {
                if (getSQ == true)
                {
                    if (c != ')')
                    {

                        cislo = cislo + c.ToString();


                    }
                    else
                    {
                        getSQ = false;
                    }


                }
                else
                {
                    if (c == '(')
                    {
                        getSQ = true;
                    }

                }


            }
            return cislo;
        }



        static string Sqrt(string cislo)
        {

            double squareRoot = Math.Sqrt(Convert.ToDouble(cislo));
            return squareRoot.ToString();
        }
        static string Power(string b)
        {
            string cisla = "";
            string varb = "";
            string result = "";
            
            foreach (char a in b)
            {

                
                    if (char.IsDigit(a))
                    {
                         cisla += a.ToString();
                    }
                    else
                    {
                         if (a !=  '.')
                    {
                        varb += a + "²";
                    }
                        
                    }
                

            }
            if (cisla.Length > 0)
            {
                cisla = (Convert.ToDouble(cisla) * Convert.ToDouble(cisla)).ToString();
                result = cisla + varb;
            }
            else
            {
                result = varb;
            }
            
            return result;
        }

    }
}
