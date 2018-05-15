defmodule Sandbox.Differentiate do
  @moduledoc """
  Documentation for Sandbox.
  """

  @doc """
  Hello world.

  ## Examples

      iex> Sandbox.hello
      :world

  """

def parsePoly(poly) do
    String.split(poly, "/")
    |> Enum.map(fn(item) ->
        {intVal, _} =  Integer.parse(item)
        intVal
    end)
end

def dropFinalTerm([]) do
    []
end

def dropFinalTerm(list) do
    {_slastTerm, restList} = List.pop_at(list, -1)
    restList
end


def translatePoly(poly) do
    poly
    |> parsePoly
    |> getDiffCoefficients
    |> polyArrayToText
end

def polyArrayToText(list) do

    {polyList, _exp} =
        Enum.reduce(list, {[], length(list) - 1}, fn(coefficient, {polyTerms, exponent}) ->
            #add to polyTerm and reduce exponent by one


            {[(ignoreUnit(Integer.to_string(coefficient)) <> expStr(exponent) <> ignoreUnit(Integer.to_string(exponent)))  | polyTerms], exponent - 1}


    end)
    Enum.join(:lists.reverse(polyList), " + ")
end

def ignoreUnit(nStr) do
    IO.inspect({:nStr, nStr})
    if nStr == "1" or nStr == "0" do
        ""
    else
        nStr
    end

end

def expStr(exp) do
    IO.inspect({:exp, exp})
    case exp do
        0 ->
            ""

        1 ->
            "x"
        _ ->
            "x^"
    end
end


def getDiffCoefficients(list) do
    list
    |> differentiate
    |> dropFinalTerm
end

def differentiate ([]) do
    []
end

def differentiate (list) do

    exp = length(list)
    {newList, _newExp} = Enum.reduce(list, {[], exp}, fn(coeff, {acc, exp}) ->
        {[coeff * (exp - 1) | acc], exp - 1}
    end)

    :lists.reverse(newList)


end


end
